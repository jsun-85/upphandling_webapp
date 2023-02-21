import requests
import urllib3
import json


url = 'https://ted.europa.eu/TED/search/search.do'

http = urllib3.PoolManager()

search = '?action=search&lgId=en&quickSearchCriteria=&searchCriteriaDto.searchScope=ARCHIVE&_searchCriteriaDto.statisticsMode=on&searchCriteriaDto.freeText=vibration&_=on&_=on&_=on&searchCriteriaDto.noticeTypeList=&searchCriteriaDto.cpvCodeList=&searchCriteriaDto.contractList=&searchCriteriaDto.nutsCodeList=&searchCriteriaDto.tenderValueMin=&searchCriteriaDto.tenderValueMax=&searchCriteriaDto.currencyList=&searchCriteriaDto.procedureList=&searchCriteriaDto.submissionLanguageList=&searchCriteriaDto.publicationDate.specificDate=&searchCriteriaDto.publicationDate.fromDate=&searchCriteriaDto.publicationDate.toDate=&searchCriteriaDto.deadlineDate.specificDate=&searchCriteriaDto.deadlineDate.fromDate=&searchCriteriaDto.deadlineDate.toDate=&searchCriteriaDto.documentationDate.specificDate=&searchCriteriaDto.documentationDate.fromDate=&searchCriteriaDto.documentationDate.toDate=&searchCriteriaDto.ojsNumber=&searchCriteriaDto.noticePublicationNumber=&searchCriteriaDto.officialName=&searchCriteriaDto.nationalRegistrationNumber=&searchCriteriaDto.countryList=SWE&searchCriteriaDto.town=&searchCriteriaDto.typeOfBuyerList=&searchCriteriaDto.mainActivityList=&_=on&_=on&_=on&_=on&_=on&searchCriteriaDto.legalBasisList=&_=on&_=on&searchCriteriaDto.fundingList='

response = requests.get(url+search)
print(response.text)

req = http.request('GET', url+search, headers={'referer': url,'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
# response = json.loads(req.data.decode())
print(req.data)