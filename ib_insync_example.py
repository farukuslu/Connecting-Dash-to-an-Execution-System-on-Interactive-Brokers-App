from ib_insync import *

ib = IB()

ib.connect(host='127.0.0.1', port=7497, clientId=3)

mgd_accets = ib.managedAccounts()



#Scanner data
allParams = ib.reqScannerParameters()
print(allParams)
sub = ScannerSubscription(
    instrument = 'FUT.US',
    locationCode='FUT.GLOBEX',
    scanCode='TOP_PERC_GAIN'
)
scanData = ib.reqScannerData(sub)
print(scanData)

#News articles
newsProviders = ib.reqNewsProviders()
print(newsProviders)

codes = '+'.join(np.code for np in newsProviders)

amd = Stock('AMD', 'SMART', 'USD')

ib.qualifyContracts(amd)

headlines = ib.reqHistoricalNews()
ib.reqNewsBulletins(True)
ib.sleep(5)