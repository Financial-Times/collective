import os, boto3, re
from requests import Session, codes
from requests.adapters import HTTPAdapter
from json import loads

def metadata_get_iam_role_name(url, mock = False):
    if mock:
        return "FT-Linux-Role"

    return get_metadata(url)
def metadata_get_region(url, mock):
    if mock:
        return "eu-west-1"
    region = self.get_metadata(url)
    return region[:-1]

def metadata_get_role(url, mock):
    if mock:
        return '''
        {
  "Code" : "Success",
  "LastUpdated" : "2017-03-02T15:19:14Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "ASIAJXZAZVBSV6E6EOFQ",
  "SecretAccessKey" : "ka2TIyd6D27oD2FRMcccn+DpxujxSX2r9XK5Mqi1",
  "Token" : "FQoDYXdzEJD//////////wEaDMcJM0u4195GYOe42iK3A0xkXCIMgH8xt8UP2+vAAKzFK71TxMsPZO4YSjiafAWJT3lQlcDFMvZGXispBBnJPCJhmLOWNVI1ChIUsN42U09+htH8A2lySncDYlnROH1zvRETVA11RLoQVP5cdMT/WO7Iti2Q994eOFqT7pj1JEJQBtI+aGqHTvKVtGzfMt5OQfkJRNbFKqFjOnvBiyhdzud7icKYm1DMWFgrCCizYuLCFaRq6E2RZ5uU+r3eTsJVr1OSeKyuN4EFkAwiH2xYKf4d/ROUYoVZt7/l/CO3NbOBkTvtXo6cAIE74ZKgtutUFVE1Q9pbFDJqIb4/+VdrHbJiRaFYAhSZvBGI5ZB07cuLd3yrq13m2EV68BG8PVdU+SwkMXTH2cEnzlD8HFr/tzGPr2QUEVMJEQZ7PJscyH8puRktaJbDtUaJjpJnJj1hgSgBjKdN1q6EK4PAGNxzphkk7uvllcJ+iDuLcaRbhJEHIAhtgsd7v/EvyiYUvxuH5GKOem9zN7tT1cjJGnKjjYNSBmpamH/P8HFevmhlkfWJt7Iet4OdCNkDjCdGMMh0lClatWcH5ah56qoiGsutmCtqrOOTnZIogPDgxQU=",
  "Expiration" : "2017-03-02T21:41:48Z"
}'''

    return get_metadata(url)

def get_metadata(request):
    """
    This method retrieves values from metadata service.

    request -- The request part after the metadata service address, for example if full request is:
               'http://169.254.169.254/latest/meta-data/placement/availability-zone/'
               then the request part is 'latest/meta-data/placement/availability-zone/'.
    """


    session = Session()
    session.mount("http://", HTTPAdapter(max_retries=2))
    result = session.get(request, timeout=5)
    if result.status_code is codes.ok:
        return str(result.text)
    else:
        print "Failed to get metadata"
        return False


def printMessage(message = "hello"):
    print message

def readKeyFromFile(key, fname):
    try:
        f = open(fname)
        lines = f.readlines()
        #print str(lines)
        for each in lines:
            neweach = each.strip().replace(" ", "") #remove control chars amd whitespace
            if re.search(key+'=', neweach):
                return neweach.split('=')[1] #Return string from right-hand side of = charachter
    except Exception, e:
        print str(e)
        return False
