import numpy as np
import pandas as pd
from bacpack.bac import Sim_BN, HFR_ETF


csim=Sim_BN(4,100000) # creating an instance of the simulation class for 3 assets and 10000 time points
csim.frequencies(10,0.2) #setting the frequencies of trades according to the simulation model
csim.generate() #generating trading data
mt=np.dot(csim.comps.T,csim.comps) #integrated covarinace matrix at highest precision to compare with
csim.noise(0.1) #generating microstructre noise
rvar=csim.fvar() # realiazed variance for each of the assets
nf_diag=csim.TSRV(2) # TSRV
noise_var=(rvar-nf_diag)/2/csim.missing_points.sum(axis=0)# estimating noise variance
noise_var=np.maximum(noise_var,0)
na_diag=2*noise_var*csim.missing_points.sum(axis=0)               
m0_RC,b0_RC=csim.HYCov() #returns RCov and implied beta                  
mweights=csim.meanw() #average weights
b0_RC_nf=b0_RC-na_diag*mweights                  
bHY=csim.beta_HY() # stock-ETF beta using Hayashi-Yoshida estimator
SBAC=m0_RC-csim.NBAC_Delta_NR(b0_RC_nf,bHY,na_diag) #BAC adjustment
m0_HY=csim.HYCov()[0]
print(m0_HY) #HY estimate of the integrated covariance matrix
print(np.linalg.norm(mt-m0_RC+np.diag(na_diag))**2,
      np.linalg.norm(mt-m0_HY+np.diag(na_diag))**2,np.linalg.norm(mt-SBAC)**2)
# squared errors of the pre-estimator and BAC

'''tmp=csim.acomps.cumsum(axis=0)
tmp[~csim.missing_points]=np.nan
tmp_etf=csim.etf.cumsum()
tmp_etf[~csim.mp_etf]=np.nan
df_prices=pd.DataFrame(np.exp(tmp),columns=["stock1","stock2","stock3","stock4"])
df_prices["ETF"]=csim.amounts.sum()+tmp_etf'''



emp=HFR_ETF()
url="https://raw.githubusercontent.com/kvdragun/bacpack/main/data/"
#url="/Volumes/SD_Card/ReplicationCode/bacpack/data/"
df_prices=pd.read_csv(url+"BAC_data.csv.zip")
emp.generate_from(df_prices,df_prices.notnull(), shnumb=np.ones(4),
                   nonequity=0, outstanding=1, etf_col="ETF")

mt=pd.read_csv(url+"truecov.csv",index_col=0)

m0_HY,b0_HY=emp.HYCov() #returns RCov and implied beta                  
bHY=emp.beta_HY() # stock-ETF beta using Hayashi-Yoshida estimator
rvar=emp.fvar() # realiazed variance for each of the assets
nf_diag=emp.TSRV(2) # TSRV
noise_var=(rvar-nf_diag)# estimating noise variance
noise_var=np.maximum(noise_var,0)            
mweights=emp.meanw() #average weights
b0_HY_nf=b0_HY-noise_var*mweights                  
SBAC=m0_HY-emp.NBAC_Delta_NR(b0_HY_nf,bHY,noise_var) #BAC adjustment 

print(np.linalg.norm(mt.values-m0_HY+np.diag(noise_var))**2,np.linalg.norm(mt.values-SBAC)**2)

#print(m0_HY,SBAC) #estimates of the integrated covariance matrix


