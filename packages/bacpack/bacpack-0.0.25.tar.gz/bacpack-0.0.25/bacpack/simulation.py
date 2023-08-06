#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 22:03:23 2017

@author: Kirill
"""
# from __future__ import absolute_import, print_function

import datetime as dt
from .highfreq import ffillz, TSRV_imp, hayo, compress
from .bac import Sim_BN

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import scipy.stats as stats
import pylab 
import statsmodels.api as sm
from numba import jit



def sim_gpu(assets=10, trades=270000, low=0.9, high=0.99, runs=np.arange(10, dtype=np.int32), noise_kappa=0,
            K=30, jumpcont=False, jumpsperiod=2, jumpmagnitude=1, jeta=25, savep=None, gpu=True,
            factor=10, minf=0.1):
    estimators = ["HY", "TSC", "RCOV", "paHY"]
    resR = pd.DataFrame(columns=
    [
        "pre-estimator",
        "data-driven"
        "oracle",
        "VAB"

    ], index=pd.MultiIndex.from_product([runs, estimators], names=["run", "estimator"]))

    csim = Sim_BN(assets, trades, low, high)
    csim.frequencies(factor, minf)
    csim.gpu = gpu
    dtn = dt.datetime.now()
    if jumpcont:
        mpsave=np.empty((trades,assets),dtype=bool)
        mpetfsave=np.empty(trades,dtype=bool)
    for l in runs:
        print(dt.datetime.now()-dtn)
        dtn = dt.datetime.now()
        csim.generate(True, fexp=False,
                      jumpsperiod=jumpsperiod, jumpgen=1 if jumpcont else 0)
        etf_nf = csim.etf.copy()
        nf_diag_01 = csim.TSRV(2)
        if noise_kappa > 0:
            csim.noise(noise_kappa)
            mm0_01 = csim.fvar()
            noise_vr = (mm0_01 - nf_diag_01) / 2 / csim.missing_points.sum(axis=0)
            noise_vr = np.maximum(noise_vr, 0)

        else:
            noise_vr = np.zeros(csim.numvar)
        print("run:", l)
        print("share of jump variance: ", csim.cumjumpvar/nf_diag_01)
        print("frequencies",csim.missing_points.sum(axis=0))
        mt = np.dot(csim.comps.T, csim.comps) #csim.ssCov
        etfvpn = (csim.letf[csim.mp_etf] ** 2).sum()
        etf_noise2 = np.maximum(etfvpn - TSRV_imp(csim.letf, csim.mp_etf, 2, 1), 0)
        if jumpcont:
            mps = csim.missing_points.sum(axis=0)
            metf = csim.mp_etf.sum()
            mpsave[:,:] = csim.missing_points[:,:]
            mpetfsave[:] = csim.mp_etf[:]
            #csim.truncate(noise=noise_kappa > 0, l_n=csim.l_n(),
            #              noise_per_observ=np.append(noise_vr, etf_noise2 / 2 / csim.mp_etf.sum()), preaver=False)
            csim.truncate_new()
            print(csim.missing_points.sum(axis=0)/mps, csim.mp_etf.sum()/metf)
        b_low = 0
        e_up = trades
        mweights = csim.meanw(b_low=b_low, e_up=e_up)
        for j in estimators:
            print("initial estimator:", j)
            na_diag = 2 * noise_vr * csim.missing_points[b_low:e_up, :].sum(axis=0)
            '''if j == "RCOV_raw":
                    m0_HY, b0_HY_W = csim.fRC2()
                    na_diag = np.zeros_like(na_diag)

            if j == "HY_raw":
                    m0_HY, b0_HY_W = csim.fHY2()
                    na_diag = np.zeros_like(na_diag)'''

            if j == "RCOV":
                    m0_HY, b0_HY_W = csim.fRC2()

            if j == "HY":
                    m0_HY, b0_HY_W = csim.fHY2()

            if j == "HY_k_n":
                    m0_HY, b0_HY_W = csim.cHY(csim.k_n())

            if j == "TSC":
                gp=csim.gpu
                csim.gpu=False
                tsc = csim.TSCov(K=K)
                csim.gpu=gp
                m0_HY = tsc
                b0_HY_W = np.dot(tsc, mweights)
                na_diag = np.zeros_like(na_diag)
                
            mtnorm = np.linalg.norm(mt)
            b_RC = csim.beta_HY()
            b_oracle = np.dot(csim.comps[csim.mp_etf, :].T, etf_nf[csim.mp_etf])

            if j == "paHY":
                if jumpcont:
                    csim.missing_points[:, :] = mpsave[:, :]
                    csim.mp_etf[:] = mpetfsave[:]
                    mps = csim.missing_points.sum(axis=0)
                    #csim.truncate(noise=noise_kappa > 0, l_n=csim.l_n())
                    csim.truncate_new(preaver=True, l_n=csim.l_n())
                    print(csim.missing_points.sum(axis=0) / mps,  csim.mp_etf.sum()/metf)
                aln=np.int32(csim.l_n()/np.sqrt(csim.numvar))
                m0_HY, b0_HY_W = csim.paHYi_beta(aln)
                b_RC=csim.pa_target_beta(aln)
                na_diag = np.zeros_like(na_diag)
                print("l_n:", csim.l_n())


            if noise_kappa > 0:
                    part_etf_noise = (e_up - b_low) / csim.numper * etf_noise2

                    na_HY = na_diag
                    b0N_HY_Wk = b0_HY_W - na_HY * mweights

                    bN_RC = b_RC  # csim.dgpu_TSCov_beta(K=50,J=10)

                    bN_VAB = b_RC + csim.fBAC_beta_log(etf_noise=part_etf_noise)

                    c_m0_NHY = m0_HY - np.diag(na_HY)

                    tmp_Delta, NL_NR = csim.NBAC_Delta_NR(b0N_HY_Wk, bN_RC, na_HY, b_low=b_low,
                                                          e_up=e_up, L_out=True)
                    c_m0_NBAC_HY_HY_NR_Wk = m0_HY - tmp_Delta
                    c_m0_NBAC_HY_oracle_NR_Wk = m0_HY - csim.NBAC_Delta_NR(b0N_HY_Wk,
                                                                            b_oracle, na_HY, L_in=True, L=NL_NR)

                    c_m0_NBAC_HY_VAB_NR_Wk = m0_HY - csim.NBAC_Delta_NR(b0N_HY_Wk,
                                                                         bN_VAB, na_HY, L_in=True, L=NL_NR)

            else:
                    b0_HY_Wk = b0_HY_W

                    b_VAB = b_RC + csim.fBAC_beta_log()
                    c_m0_NHY = m0_HY

                    tmp_Delta, L_NR = csim.BAC_Delta_NR(b0_HY_Wk, b_RC, b_low=b_low,
                                                        e_up=e_up, L_out=True)
                    c_m0_NBAC_HY_HY_NR_Wk = m0_HY - tmp_Delta

                    c_m0_NBAC_HY_oracle_NR_Wk = m0_HY - csim.BAC_Delta_NR(b0_HY_Wk,
                                                                          b_oracle, L_in=True, L=L_NR)

                    c_m0_NBAC_HY_VAB_NR_Wk = m0_HY - csim.BAC_Delta_NR(b0_HY_Wk, b_VAB,
                                                                       L_in=True, L=L_NR)

            resR.loc[(l, j), "pre-estimator"] = np.linalg.norm(mt - c_m0_NHY) ** 2 / mtnorm ** 2
            print(resR.loc[(l, j), "pre-estimator"])
            resR.loc[(l, j), "data-driven"] = np.linalg.norm(mt - c_m0_NBAC_HY_HY_NR_Wk) ** 2 / mtnorm ** 2
            resR.loc[(l, j), "oracle"] = np.linalg.norm(mt - c_m0_NBAC_HY_oracle_NR_Wk) ** 2 / mtnorm ** 2
            resR.loc[(l, j), "VAB"] = np.linalg.norm(mt - c_m0_NBAC_HY_VAB_NR_Wk) ** 2 / mtnorm ** 2

            if savep != None:
                nj = "_noise%.2f" % noise_kappa if noise_kappa > 0 else ""
                nj += "_jump" if jumpcont else ""
                if not os.path.exists(savep + "%d" % assets + j + nj):
                    os.mkdir(savep + "%d" % assets + j + nj)

                np.savez_compressed(savep + "%d" % assets + j + nj + "/_%d" % l,
                                        npreest=c_m0_NHY,
                                        NBAC_HY=c_m0_NBAC_HY_HY_NR_Wk,
                                        NBAC_oracle=c_m0_NBAC_HY_oracle_NR_Wk,
                                        NBAC_VAB=c_m0_NBAC_HY_VAB_NR_Wk)


        if savep != None:
            if not os.path.exists(savep + "%d" % assets + "TRUE" + nj):
                os.mkdir(savep + "%d" % assets + "TRUE" + nj)
            np.savez_compressed(savep + "%d" % assets + "TRUE" + nj + "/_%d" % l,
                                true=csim.ssCov,
                                mt=mt)
    if savep != None:
        resR.to_excel(savep + "res" + "%d" % assets + nj + ".xlsx")
    return resR / len(runs)


sim_gpu(assets=10, noise_kappa=0.085, trades=23400, factor = 10,
minf = 0.075, runs=range(1000), jumpcont=True, savep="/Users/Cyrus/Desktop/BAC_l_n_2/")
'''sim_gpu(assets=30, noise_kappa=0.085, trades=23400, factor = 10,
minf = 0.075, runs=range(1000), jumpcont=True, savep="/Users/Cyrus/Desktop/BAC_l_n_3/")
sim_gpu(assets=100, noise_kappa=0.085, trades=23400, factor = 10,
minf = 0.075, runs=range(1000), jumpcont=True, savep="/Users/Cyrus/Desktop/BAC_l_n_3/")'''

'''sim_gpu(10, 23400,  runs=np.arange(1000, dtype=np.int32), noise_kappa=0.085, gpu=False,
        jumpcont=False, jumpsperiod=2, savep="/Users/Cyrus/Desktop/BAC_redo/")
sim_gpu(10, 23400,  runs=np.arange(1000, dtype=np.int32), noise_kappa=0.085, gpu=False,
        jumpcont=True, jumpsperiod=2, savep="/Users/Cyrus/Desktop/BAC_redo/")'''


def sim_gpu_noise(assets=10, trades=23400, low=0.9, high=0.99, runs=np.arange(10),
                  noise_kappa=np.arange(0,0.2,0.01), K=30, jumpcont=True, jumpsperiod=2,
                  jumpmagnitude=1, jeta=25, savep="/Users/Cyrus/Desktop/BAC_noise/", gpu=True,
                  factor=10, minf=0.02):
    resR = pd.DataFrame(np.zeros((len(noise_kappa), 17)), index=
    noise_kappa, columns=['paHY','HY', 'RC', 'TSC', 'paHYJ',"HYJ", "RCJ", "TSCJ",
                          "opaHY",'oHY', 'oRC', 'oTSC',"opaHYJ", "oHYJ", "oRCJ", "oTSCJ", "adj"])
    csim = Sim_BN(assets, trades, low, high)
    csim.frequencies(factor, minf)
    csim.gpu = gpu
    if jumpcont:
        mpsave=np.empty((trades,assets),dtype=bool)
        mpetfsave=np.empty(trades,dtype=bool)
    for l in runs:
        for jmp in range(2 if jumpcont else 1):
            csim.generate(True, fexp=False,
                              jumpsperiod=jumpsperiod, jumpgen=jmp)
            sacomps = csim.acomps.copy()
            sletf = csim.letf.copy()
            setf = csim.etf.copy()
            print(dt.datetime.now())
            for jns in resR.index:
                print(jns, l)
                csim.acomps[:,:] = sacomps
                csim.letf[:] = sletf
                csim.etf[:] = setf
                etf_nf = csim.etf.copy()
                if jns > 0:
                    csim.noise(jns)
                mm0_01 = csim.fvar()
                nf_diag_01 = csim.TSRV(2)
                noise_vr = (mm0_01 - nf_diag_01) / 2 / csim.missing_points.sum(axis=0)
                noise_vr = np.maximum(noise_vr, 0)
                print("run:", l)
                mt = np.dot(csim.comps.T, csim.comps)
                adj = 1
                '''if jumpcont and jmp == 1:
                    etfvpn = (csim.letf[csim.mp_etf] ** 2).sum()
                    etf_noise2 = np.maximum(etfvpn - TSRV_imp(csim.letf, csim.mp_etf, 2, 1), 0)

                    adj = csim.numper / (csim.numper - csim.jumpsfree(nf_diag_01,
                                                                      noise_vr, etfvpn,
                                                                      etf_noise2 / 2 / csim.mp_etf.sum()))
                    mm0_01 = csim.fvar()
                    nf_diag_01 = csim.TSRV(2)
                    noise_vr = (mm0_01 - nf_diag_01) / 2 / csim.missing_points.sum(axis=0)
                    noise_vr = np.maximum(noise_vr, 0)'''
                
                    
                etfvpn = (csim.letf[csim.mp_etf] ** 2).sum()
                etf_noise2 = np.maximum(etfvpn - TSRV_imp(csim.letf, csim.mp_etf, 2, 1), 0)
                if jumpcont and jmp == 1:
                    mps = csim.missing_points.sum(axis=0)
                    mpsave[:,:] = csim.missing_points[:,:]
                    mpetfsave[:]= csim.mp_etf[:]
                    csim.jtruncate(nf_diag_01, noise_vr, etfvpn, etf_noise2 / 2 / csim.mp_etf.sum())
                    print(csim.missing_points.sum(axis=0)/mps)    
                
                print("etf_noise:", etf_noise2, "adj : ", adj)
                for j in range(3,-1,-1):
                    sest = ["paHY","HY", "RC", "TSC"][j]
                    print("initial estimator:", j)
                    c_m0_HY = np.zeros((csim.numvar, csim.numvar))
                    c_m0_NHY = np.zeros((csim.numvar, csim.numvar))

                    c_m0_NBAC_HY_HY_NR_Wk = np.zeros((csim.numvar, csim.numvar))
                    c_m0_NBAC_HY_oracle_NR_Wk = np.zeros((csim.numvar, csim.numvar))
                    c_m0_NBAC_HY_VAB_NR_Wk = np.zeros((csim.numvar, csim.numvar))

                    b_low = 0
                    e_up = trades

                    if True:
                        na_diag = 2 * noise_vr * csim.missing_points[b_low:e_up, :].sum(axis=0)
                        mweights = csim.meanw(b_low=b_low, e_up=e_up)

                        if sest == "RC":
                            m0_HY, b0_HY_W = csim.fRC2()

                        if sest == "HY":
                            m0_HY, b0_HY_W = csim.fHY2()

                        if sest == "TSC":
                            gp=csim.gpu
                            csim.gpu=False
                            tsc = csim.TSCov(K=K)
                            csim.gpu=gp
                            m0_HY = tsc
                            b0_HY_W = np.dot(tsc, mweights)
                            na_diag = np.zeros_like(na_diag)
                            
                        b_RC = csim.beta(b_low=b_low, e_up=e_up)   
                        
                        if sest == "paHY":

                                if jumpcont and jmp == 1:
                                    csim.missing_points[:,:]=mpsave[:,:]
                                    csim.mp_etf[:]=mpetfsave[:]
                                    mps = csim.missing_points.sum(axis=0)
                                    csim.truncate(noise=True, l_n=csim.l_n())
                                    print(csim.missing_points.sum(axis=0)/mps)
                                aln=np.int32(csim.l_n()/np.sqrt(csim.numvar))
                                m0_HY, b0_HY_W = csim.paHYi_beta(aln)
                                b_RC=csim.pa_target_beta(aln)
                                na_diag = np.zeros_like(na_diag)
                                print("l_n:", csim.l_n())
                        
                        b_oracle = np.dot(csim.comps[csim.mp_etf, :].T, etf_nf[csim.mp_etf])
                        part_etf_noise = (e_up - b_low) / csim.numper * etf_noise2

                        na_HY = na_diag
                        b0N_HY_Wk = b0_HY_W - na_HY * mweights

                        bN_RC = b_RC  # csim.dgpu_TSCov_beta(K=50,J=10)
                        bN_VAB = b_RC + csim.fBAC_beta_log(etf_noise=part_etf_noise)

                        c_m0_NHY += m0_HY - np.diag(na_HY)

                        tmp_Delta, NL_NR = csim.NBAC_Delta_NR(b0N_HY_Wk, bN_RC, na_HY, b_low=b_low,
                                                              e_up=e_up, L_out=True)
                        c_m0_NBAC_HY_HY_NR_Wk = m0_HY - tmp_Delta
                        c_m0_NBAC_HY_oracle_NR_Wk += m0_HY - csim.NBAC_Delta_NR(b0N_HY_Wk,
                                                                                b_oracle, na_HY, L_in=True, L=NL_NR)
                        c_m0_NBAC_HY_VAB_NR_Wk += m0_HY - csim.NBAC_Delta_NR(b0N_HY_Wk,
                                                                             bN_VAB, na_HY, L_in=True, L=NL_NR)
                        c_m0_NHY *= adj
                        c_m0_NBAC_HY_HY_NR_Wk *= adj
                        # c_m0_NBAC_HY_oracle_NR_Wk*=adj
                        c_m0_NBAC_HY_VAB_NR_Wk *= adj

                    if savep != None:
                        nj = "_noise%.3f" % jns
                        nj += "_jump" if jumpcont and jmp == 1 else ""
                        if not os.path.exists(savep + "%d" % assets + sest + nj):
                            os.mkdir(savep + "%d" % assets + sest + nj)
                        np.savez_compressed(savep + "%d" % assets + sest + nj + "/_%d" % l,
                                            preest=c_m0_HY,
                                            npreest=c_m0_NHY,
                                            NBAC_HY=c_m0_NBAC_HY_HY_NR_Wk,
                                            NBAC_oracle=c_m0_NBAC_HY_oracle_NR_Wk,
                                            NBAC_VAB=c_m0_NBAC_HY_VAB_NR_Wk)
                    if not os.path.exists(savep + "%d" % assets + "TRUE" + nj):
                        os.mkdir(savep + "%d" % assets + "TRUE" + nj)
                    np.savez_compressed(savep + "%d" % assets + "TRUE" + nj + "/_%d" % l,
                                        true=csim.ssCov,
                                        highprec=mt)
                    print(np.linalg.norm(mt - c_m0_NHY) ** 2)
                    resR.loc[jns, resR.columns[j + jmp * 4]] += (np.linalg.norm(mt - c_m0_NHY) ** 2 /
                                                                 np.linalg.norm(mt - c_m0_NBAC_HY_VAB_NR_Wk) ** 2)
                    resR.loc[jns, resR.columns[j + jmp * 4 + 8]] += (np.linalg.norm(mt - c_m0_NHY) ** 2 /
                                                                     np.linalg.norm(
                                                                         mt - c_m0_NBAC_HY_oracle_NR_Wk) ** 2)
                    resR.loc[jns, "adj"] += adj

                if jumpcont and jmp == 1:
                    csim.missing_points[:, :] = mpsave[:, :]
                    csim.mp_etf[:] = mpetfsave[:]
                    
    (resR / len(runs)).to_excel(savep + "noise_sensitivity.xlsx")
    return resR / len(runs)

#sim_gpu_noise(assets=30,runs=range(885,1000))

