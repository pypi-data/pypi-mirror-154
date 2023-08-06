__all__ = ['LogisticRegressionCalibrator', 'LogisticRegressionCalibratorPlatt', 'IsotonicRegressionCalibrator',"BinningCalibrator"]

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from functools import partial
import multiprocessing as mp
import os
from decimal import Decimal
import warnings
import time
import sys
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import LocalOutlierFactor
from pyod.models.abod import ABOD
from pyod.models.iforest import IForest

class LogisticRegressionCalibratorPlatt:
    A = 0
    B = 0

    def __init__(self):
        pass

    def train(self, h0, h1, withLinFix=True):
        #fits a LR model, defined by weight self.A and score self.B, to scores h0 and h1. See https://en.wikipedia.org/wiki/Platt_scaling
        #Assumes labels of h0 is 0 (normal) and labels of h1 is 1 (anamolous)
        #expects single dimensional arrays of anyform (list, numpy, mx1, 1xm, etc.)

        n0 = np.size(h0)
        n1 = np.size(h1)
        H = np.append(np.reshape(h0, n0), np.reshape(h1, n1))
        H = H.reshape(n0 + n1, 1)
        tp = (n1 + 1) / (n1 + 2)
        tn = 1/(n0+2)
        t = np.array(([tn] * n0) + ([tp] * n1))
        self.fit(H, t, n0, n1)

    def test(self, H):
        #Reutrns the predicted posterioir probabilities of the list of scores H using the fitted LR model
        #expects single dimensional array of anyform (list, numpy, mx1, 1xm, etc.)
        #   Arguments:
        #       H - classifier scores

        H = np.array(H)
        n = np.size(H)
        H = H.reshape(n, 1)
        return 1/(1+np.exp(H*self.A + self.B))

    def fit(self, H, t, n0, n1):
        """
        The folllowing has been converted from psuedo code given in Lin HT, Lin CJ, Weng R. A note on platt's probabilistic outputs for support vector machines. Mach Learn. 2007; 68:267–276.

        Input parameters:
            H = array of scores
            t = array of adjusted targets
            n1 = number of positive examples
            n0 = number of negative examples
        Outputs:
            A, B = parameters of sigmoid
        """

        #Parameter setting
        maxiter=10000 #Maximum number of iterations
        minstep=1e-10 #Minimum step taken in line search
        sigma=1e-12 #Set to any value > 0

        len=n0+n1 #total data set size

        A=0.0
        B=np.log((n0+1.0)/(n1+1.0))
        fval=0.0
        for i in range(len):
            fApB=H[i]*A+B #Ay+B
            if (fApB >= 0):
                fval += t[i]*fApB+np.log(1+np.exp(-fApB)) # y(Ay+B) + log(1+e^(-Ay+B))
            else:
                fval += (t[i]-1)*fApB+np.log(1+np.exp(fApB)) # (y-1)(Ay+B) + log(1+e^(Ay+B)

        for it in range(maxiter):
            #Update Gradient and Hessian (use H’ = H + sigma I)
            h11=h22=sigma
            h21=g1=g2=0.0
            for i in range(len):
                fApB=H[i]*A+B #Ay+B
                if (fApB >= 0):
                    p=np.exp(-fApB)/(1.0+np.exp(-fApB))     # p = e^(-Ay+B)/1+e^(-Ay+B)
                    q=1.0/(1.0+np.exp(-fApB))               # q = 1/1+e^(-Ay+B)
                else:
                    p=1.0/(1.0+np.exp(fApB))                # p = 1/1+e^(Ay+B)
                    q=np.exp(fApB)/(1.0+np.exp(fApB))       # q = e^(Ay+B)/1+e^(Ay+B)
                d2=p*q
                h11 += H[i]*H[i]*d2
                h22 += d2
                h21 += H[i]*d2
                d1 = t[i]-p
                g1 += H[i]*d1
                g2 += d1
            if ( abs(g1)<1e-5 and abs(g2)<1e-5 ): #Stopping criteria
                break

            #Compute modified Newton directions
            det=h11*h22-h21*h21
            dA=-(h22*g1-h21*g2)/det
            dB=-(-h21*g1+h11*g2)/det
            gd=g1*dA+g2*dB
            stepsize=1
            while (stepsize >= minstep): #Line search
                newA=A+stepsize*dA
                newB=B+stepsize*dB
                newf=0.0
                for i in range(len):
                    fApB=H[i]*newA+newB #A'y+B'
                    if (fApB >= 0):
                        newf += t[i]*fApB+np.log(1+np.exp(-fApB)) # y(A'y+B') + log(1+e^(-(A'y+B')))
                    else:
                        newf += (t[i]-1)*fApB+np.log(1+np.exp(fApB)) # (y-1)(A'y+B') + log(1+e^(A'y+B'))

                if (newf < (fval+0.0001*stepsize*gd) ):
                    A=newA
                    B=newB
                    fval=newf
                    break #Sufficient decrease satisfied
                else:
                    stepsize /= 2.0
            if (stepsize < minstep):
                print("Line search fails")
                break
        if (it >= maxiter):
            print("Reaching maximum iterations")

        self.A = A
        self.B = B

        return 0

    def toString(self):
        return "Platt"


class LogisticRegressionCalibrator:
    Ext=False
    scaler=None

    def __init__(self,  exstensible=False):
        #set extensible to True to add extra feature(s) x^2 (mono clf case) and x1^2, x2^2, x1*x2 (multi clf case)
        self.Calibrator = LogisticRegression(solver='lbfgs', n_jobs=1)
        self.Ext = exstensible

    def train(self, h0, h1,):
        #fits the LR model, self.Calibrator, to scores h0 and h1. Assumes labels of h0 is 0 (normal) and labels of h1 is 1 (anamolous)
        #expects single dimensional arrays of anyform (list, numpy, mx1, 1xm, etc.)

        h0 = np.array(h0)
        h1 = np.array(h1)

        n0 = h0.shape[0]
        n1 = h1.shape[0]
        H = np.append(h0, h1, axis=0)
        if not len(H.shape) > 1: #add column dimension
            H = H.reshape(H.shape[0], 1)

        assert H.shape[1] in [1,2], "training data has wrong shape, must be n rows by 2 columns for multi-score calibration!"

        y = np.append(np.zeros(n0), np.ones(n1)) #labels

        if self.Ext == True:
            H = np.concatenate( (H, H**2), 1) #add squared column(s)
            if H.shape[1] > 2: #if multi classifier calibration
                H = np.concatenate( (H, np.reshape(H[:,0]*H[:,1], (H.shape[0],1) ) ), 1) #add x1*x2
            mms = MinMaxScaler()
            mms.fit(H.astype(float))
            H = mms.transform(H) #scale data to 0,1 range
            self.scaler = mms #save scaler

        self.Calibrator.fit(H,y)


    def test(self, H):
        #Reutrns the predicted posterioir probabilities of the list of scores H using the fitted LR model, self.Calibrator
        #expects single dimensional array of anyform (list, numpy, mx1, 1xm, etc.)
        #   Arguments:
        #       H - classifier scores

        H = np.array(H)
        if not len(H.shape) > 1: #add column dimension
            H = H.reshape(H.shape[0], 1)

        if self.Ext:
            H = np.concatenate( (H, H**2), 1) #add squared column
            if H.shape[1] > 2: #if multi classifier calibration
                H = np.concatenate( (H, np.reshape(H[:,0]*H[:,1], (H.shape[0],1) ) ), 1) #add squared column
            H = self.scaler.transform(H) #scale data
        return( self.Calibrator.predict_proba(H)[:,1] )

    def toString(self):
        if self.Ext == True:
            return "LogisticExtensible"
        else:
            return "Logistic"


class IsotonicRegressionCalibrator:

    def __init__(self):
      self.Calibrator = IsotonicRegression(out_of_bounds='clip')

    def train(self, h0, h1):
        #fits the IR model, self.Calibrator, to scores h0 and h1. Assumes labels of h0 is 0 (normal) and labels of h1 is 1 (anamolous)
        #expects single dimensional arrays of anyform (list, numpy, mx1, 1xm, etc.)

        n0 = np.size(h0)
        n1 = np.size(h1)
        H = np.append(np.reshape(h0, n0), np.reshape(h1, n1))

        y = np.append(np.zeros(n0), np.ones(n1)) #labels

        self.Calibrator.fit(H,y)


    def test(self, H):
        #Reutrns the predicted posterioir probabilities of the list of scores H using the fitted IR model in self.Calibrator.
        #expects single dimensional array of anyform (list, numpy, mx1, 1xm, etc.)
        #   Keyword arguments:
        #       H - classifier scores

        return self.Calibrator.predict(H)

    def toString(self):
        return "Isotonic"


class BinningCalibrator:
    descrete = False
    EPS = np.finfo(float).eps #min. precision: y/(x+eps) will guard against DBZ error when x=0.


    def __init__(self, descrete=False, n_bins=10):
        #set descrete = True for descrete valued scores, and false for continious valued scores
        #n_bins determines the number of equal width bins only for contious valued scores, otherwise this variable is ignored

        self.descrete = descrete
        self.n_bins=n_bins

    def train(self, h0, h1):
        #Gets nonparametric MLE posterioir for a set of equal width bings from scores h0 and h1. Assumes labels of h0 is 0 (normal) and labels of h1 is 1 (anamolous)
        #expects single dimensional arrays of anyform (list, numpy, mx1, 1xm, etc.)

        n0 = np.size(h0)
        n1 = np.size(h1)
        H = np.append(np.reshape(h0, n0), np.reshape(h1, n1))
        H = H.reshape(n0 + n1, 1)
        Hmin =  np.amin(H)
        Hmax = np.amax(H)

        if self.descrete:
            # descrete scores assume to be element of all integer values from Hmin to Hmax
            bw = 1 #bin width
            self.n_bins = np.unique(H).shape[0] #number of bins equal to number of classes
            self.bin_edges = np.arange(0, self.n_bins+1, bw) - bw/2 #bins

        else:
            self.bin_edges, _ = np.linspace(Hmin, Hmax, self.n_bins+1, retstep=True)

        lhr = np.zeros(self.n_bins)
        counts0, bins0 = np.histogram(h0, bins=self.bin_edges, density=True) #histogram of nefative class
        counts1, bins1 = np.histogram(h1, bins=self.bin_edges, density=True) #histogram of positive class

        p = n1/(n1 + n0) #prior
        for i in range(lhr.shape[0]):
            if counts0[i] == 0 and counts1[i] != 0:# 1/0 = ∞
                lhr[i] = np.inf
            elif counts0[i] != 0 and counts1[i] == 0:# 0/1 = 0
                lhr[i] = 0
            elif counts0[i] == 0 and counts1[i] == 0:# 0/0 = ( (leftPosCount + rightPosCount)/(2+n) )  /  ( (leftNegCount + rightNedCount)/(2+n) ) # where n is number of 0/0 bins. Note: 2+n cancels out thus is irrelevant
                lhr[i] = -1 #replaced with true value later
            else:
                lhr[i] = counts1[i]/counts0[i]         #nonparametric MLE lhr ratio of number of observations in each bin.

        j = 0
        for i in range(lhr.shape[0]):
            if lhr[i] == -1: #count number of bins which evaluated to 0/0 in current run
                j+=1
            elif j > 0: #if end of run of 0/0 bins
                if (counts0[i-j-1]+counts0[i]) == 0: #if rightBin and leftBin both = ∞
                    for k in range(1,j+1): #all 0/0 bins' lhr estimate set to ∞
                       lhr[i-k] = np.inf
                else:
                    for k in range(1,j+1): #use counts in left and right bin to set all 0/0 bins' lhr estimate
                        lhr[i-k] = (counts1[i-j-1]+counts1[i])/(counts0[i-j-1]+counts0[i])
                j = 0 #no longer in run of 0/0 bins

        self.pmle = 1/(1+ (lhr + self.EPS)**-1 * (1-p)/p)  #nonparametric MLE posterioir for each bin.

    def test(self, H):
        #Reutrns the predicted posterioir probabilities of the list of scores H using the fitted IR model in self.Calibrator.
        #expects single dimensional array of anyform (list, numpy, mx1, 1xm, etc.)
        #   Keyword arguments:
        #       H - classifier scores

        H = np.array(H)
        n = np.size(H)
        H = H.reshape(n, 1)

        tempPmle = np.concatenate(([self.pmle[0]],self.pmle,[self.pmle[-1]]))
        y = tempPmle[np.searchsorted(self.bin_edges, H)]
        return y

    def toString(self):
        return "Binning("+str(self.n_bins)+")"

__all__ = ['getAllNCDFs', 'unavoidsScore']


def getNCDF(X, p, index):
    """
    Calculate the NCDF for a single sample using a specified norm

    Parameters:
    X (n x m numpy array): an array containing n samples and m feature values, assumed to be normalized between 0 and 1
    p (float): the norm to use when calculating the distance between points
    index (int): the index of the sample in X which we are finding the NCDF for

    Returns:
    NCDFxi (1 x n numpy array): where the n^th value equals NCDF_xi(n)
    """

    n = X.shape[0]
    d = X.shape[1]

    with warnings.catch_warnings():
        try:
            warnings.filterwarnings('error')

            NCDFxi = np.zeros((1, n))  # matrix to hold NCDF

            if p == np.inf:
                NCDFxi[0,:] = ( np.max(np.abs(X[index,:]-X[:,:]), axis=1)) #calculate Chebyshev distance between sample X[i] and X[j != i]
            else:
                NCDFxi[0,:] = ( np.sum(np.abs(X[index,:]-X[:,:])**p, axis=1)**(1.0/float(p))) #calculate p-norm of samples X[i] and X[j != i]

            #normalize by max volumne
            maxNorm = np.max(NCDFxi[0,:])
            if maxNorm  > 0:
                NCDFxi[0,:] = NCDFxi[0,:]/maxNorm

            NCDFxi = np.sort(NCDFxi, axis=1)

        except Warning as e:
            print("Warning: "+str(e)+" -> switching to from numpy to Decimal library implementation, expect speed decrease.\n\tAny further warnings mean results may be incorrect.")

            NCDFxi = []  # array to hold NCDF

            for I in range(n):
                if p == np.inf:
                    NCDFxi.append(( np.max(np.abs(X[index,:]-X[I,:])) )) #calculate Chebyshev distance between sample X[i] and X[j != i]
                else:
                    NCDFxi.append(Decimal(( np.sum(np.abs(X[index,:]-X[I,:])**p)))**Decimal(1.0/float(p))) #/ (d**(1.0/p)) #calculate p-norm of samples X[i] and X[j != i]

            #normalize by max volumne
            maxNorm = max(NCDFxi)
            if maxNorm > 0:
                for I in range(n):
                    NCDFxi[I] = NCDFxi[I]/maxNorm

            NCDFxi = np.array(NCDFxi.sort()).reshape((1, n))

    return NCDFxi

def getAllNCDFs(X, p=0.0625, ncpus=4):
    """
    Calculate the NCDF for all samples in parallel using a specified norm

    Parameters:
    X (n x m numpy array): an array containing n samples and m feature values
    p (float): the norm to use when calculating the distance between points
    ncpus (int): the number of parallel processes

    Returns:
    NCDF (n x n numpy array): the n^th row equals the NCDF for the nth sample in X
    """

    if np.amax(X) != 1.0 or np.amax(X) != 0:

        #normalize features between 0 and 1
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)

    #catch overflows, underflows and invalid values and invalid division
    np.errstate(all='raise')
    np.seterr(all='raise')

    #get NCDFs
    pool = mp.Pool(processes=ncpus)
    func = partial(getNCDF, X, p) #pass X and p as first two args of getNCDF
    result = pool.map(func, range(X.shape[0])) #run getNCDF in parallel across each sample
    pool.close()
    pool.join()

    return np.reshape(result, (X.shape[0],X.shape[0]))

def getBetaFractions(NCDFs_L, BetaSorted, BetaRanks, fraction_WSS, index):
    """
    Calculate the UNVAOIDS outlier score for a given sample using the fractions of all gaps method

    Parameters:
    NCDFs_L (n x L numpy array): an array containing the intercepts for n NCDFs at L beta levels
    BetaSorted (n x L numpy array): the same as NCDFs_L but the intercepts are sorted along the L beta levels (columize sort of NCDFs_L)
    BetaRanks (n x L numpy array): the same as NCDFs_L but the value at (i,j) is replaced with the rank of NCDFs_L[i,j] on a given beta horizontal
    Fractions_WSS: the number of nearest intercepts to be encompossased by the gap whose size will be the score for the given beta and NCDF's intercept
    index (int): the index of the NCDF in X which we are finding the score for

    Returns:
    score (1 x 1 numpy array): equal to the score for current samples across all beta levels
    """

    n = NCDFs_L.shape[0] #number of Betas
    L = NCDFs_L.shape[1] #number of NCDFs

    k_gaps = np.zeros((L,1))

    #for each column
    for col in range(L):
        obser_intercept = NCDFs_L[index,col] #get intercept of this NCDF
        obser_rank = BetaRanks[index,col] #get rank of inercept for this NCDF

        #get nearest(by rank) fraction_WSS * 2 intercepts
        if obser_rank - fraction_WSS < 0:
            bottom = 0
            top =  obser_rank + fraction_WSS + 1 - (obser_rank - fraction_WSS)
        elif obser_rank + fraction_WSS + 1 > n:
            bottom = obser_rank - fraction_WSS - ((obser_rank + fraction_WSS + 1) - n)
            top =  n
        else:
            bottom = obser_rank - fraction_WSS
            top = obser_rank + fraction_WSS + 1

        #sort only the gaps to the k_max * 2 nearest intercepts
        gaps = np.sort(np.abs(BetaSorted[bottom:top,col] - obser_intercept))

        #get gaps for each Fraction
        k_gaps[col,0] = gaps[fraction_WSS]

    #get largest gap metrix
    score = np.amax(k_gaps,axis=0)

    return score

    return k_gaps

def getBetasHist(NCDFs_L, BetaSorted, index):

    """
    Calculate the UNVAOIDS outlier score for a given sample using the histogram method

    Parameters:
    NCDFs_L (n x L numpy array): an array containing the intercepts for n NCDFs at L beta levels
    BetaSorted (n x L numpy array): the same as NCDFs_L but the intercepts are sorted along the L beta levels (columize sort of NCDFs_L)
    index (int): the index of the NCDF in X which we are finding the score for

    Returns:
    score (1 x 1 numpy array): equal to the score for current samples across all beta levels
    """

    n = NCDFs_L.shape[0] #number of NCDFs
    L = NCDFs_L.shape[1] #number of Betas

    beta_max = 0 #the highest score of the beta levels

    n_bins = n * 0.05
    step = 1/n_bins

    for col in range(1, L-1):
        obser_intercept = NCDFs_L[index,col] #intercept of observation
        hrzntl = NCDFs_L[:,col]              #current beta level

        #center obeservation intercept in bin with width 0.05
        lb = obser_intercept - 0.025
        ub = obser_intercept + 0.025

        #create the rest of the bins between 0 and 1 with widths 0.05, edge bins may be cut off by subceeding 0 or exceeding 1
        edges = [0,1.01]
        n_le = 1 #number of edges below observation
        while True:
            if lb <= 0:
                break
            else:
                n_le += 1
                edges.append(lb)
                lb -= step

        while True:
            if ub >= 1:
                break
            else:
                edges.append(ub)
                ub += step
        edges.sort() #sort edges

        #create histogram and get bin counts
        hist = np.zeros((len(edges)-1,1))
        cur_count = 0
        cur_edge = 1

        for intercept in BetaSorted[:,col]:
            while True:
                if intercept <= edges[cur_edge]: #if current sample is less then cur edge, add to cur bin
                    hist[cur_edge-1] += 1 #increment bin counter
                    break #break when you find the sample's bin
                else: #else look at next edege/bin
                    cur_edge +=1

        #determine score
        score = 0
        for i in hist:
            if (hist[n_le-1] < i[0]):
                score += i[0]
        beta = score/n

        #compare with best score so far
        if beta > beta_max:
            beta_max = beta

    return np.array(beta_max).reshape((1,1))

def unavoidsScore(X, precomputed=False, p=0.0625, returnNCDFs=True, method="fractions", r=0.01,  L=100, ncpus=4):

    """
    Calculate the UNVAOIDS outlier score for a all samples

    Parameters:
    X (n x m numpy array): an array containing n samples and m feature values
    precomputed (boolena): if True, X is assumed to be the NCDF array returnd by getAllNCDFs
    p (float): the norm to use when calculating the distance between points
    returnNCDFs(boolean): if True, NCDF array is returned along with outlier scores
    method (string): specifies which method to use for ccalculating outlier scores; either "fractions" or "histogram"
    r: percentage of nearest intercepts to be encompossased by the gap whose size will be the score for the given beta and NCDF's intercept when using the "fractions" method
    L (int): the number of beta levels to use
    ncpus (int): the number of parallel processes

    Returns:
    scores (n x 1 numpy array): where the n^th element is equal to the score for the n^th sample in X
    NCDFs (n x n numpy array): only returned if returnNCDFs == True. The n^th row equals the NCDF for the nth sample in X
    """

    if precomputed == False:
        NCDFs = getAllNCDFs(X, p)

    WSS = NCDFs.shape[0]

    Lindexes = np.unique(np.append(np.floor(np.arange(0,L)*(WSS/L)), WSS-1).astype(int)) #indicies of beta levels
    Fractions_WSS = int((r * WSS))  #convert percentage to proption of window size

    NCDFs_L = NCDFs[:, Lindexes] #for current norm, grab all NCDF intercepts with all L beta levels
    BetaSorted = np.sort(NCDFs_L, axis=0) #sort intercepts along beta level
    BetaRanks = np.argsort((np.argsort(NCDFs_L, axis=0)), axis=0) #get ranks of intercepts

    if method == "fractions":
        #get score for each sample and all fractions using Fractions method
        pool = mp.Pool(processes=ncpus)
        func = partial(getBetaFractions, NCDFs_L, BetaSorted, BetaRanks, Fractions_WSS)
        scores = np.array(pool.map(func, range(NCDFs_L.shape[0])))
        pool.close()
        pool.join()

    elif method == "histogram":
        #get best beta using Histogram approaches
        pool = mp.Pool(processes=ncpus)
        func = partial(getBetasHist, NCDFs_L, BetaSorted)
        scores = np.array(pool.map(func, range(0, NCDFs_L.shape[0])))
        pool.close()
        pool.join()

    if returnNCDFs == False:
        return scores.reshape((NCDFs.shape[0], -1))
    else:
        return scores.reshape((NCDFs.shape[0], -1)), NCDFs
