#   Copyright 2022 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import requests
import argparse
from bs4 import BeautifulSoup

def getBaseUrl(url):
  baseUrlIndex = url.rfind("/")
  baseUrl = url
  if baseUrlIndex != -1:
    baseUrl =  url[0:baseUrlIndex+1]
  return baseUrl

def getLinks(articleUrl, result):
  if result == None:
    result = {}
  res = requests.get(articleUrl)
  baseUrl = getBaseUrl(articleUrl)
  soup = BeautifulSoup(res.text, 'html.parser') #use html instead of res.text
  links = soup.find_all("a", {})
  for aLink in links:
    theUrl = aLink.get("href").strip()
    theText = aLink.get_text().strip()
    if theText=="Next" and theUrl.find("tab=repositories")!=-1:
      result = getLinks( theUrl, result )
    else:
      theItemProp = aLink.get("itemprop")
      if theItemProp == "name codeRepository":
        result[theText] = baseUrl+theUrl
  return result


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Parse command line options.')
  parser.add_argument('args', nargs='*', help='list up github account e.g. hidenoly')
  parser.add_argument('-m', '--mode', action='store', default='dump', help='specify mode dump or clone')

  args = parser.parse_args()

  links = {}
  baseUrl = "https://github.com/"

  accounts = sys.argv
  del accounts[0]

  for anAccount in accounts:
    links = getLinks(baseUrl+anAccount+"?tab=repositories", links)

  for theText, theUrl in links.items():
    if args.mode == "dump":
      print('  "'+theText+'":"'+theUrl+'",')
    elif args.mode == "clone":
      print("git clone "+theUrl)
