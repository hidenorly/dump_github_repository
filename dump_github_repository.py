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
import re
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

  _result = []
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
        _result.append( { "name": theText, "url":baseUrl+theUrl, "lang":""} )

  langs = soup.find_all("span", {})
  result_lang = []
  for aLang in langs:
    theItemProp = aLang.get("itemprop")
    if theItemProp == "programmingLanguage":
      result_lang.append( aLang.get_text().strip() )

  i = 0
  nLangMax = len(result_lang)
  for aData in _result:
    tmp = aData
    if i < nLangMax:
      tmp["lang"] = result_lang[i]
    result[ aData["name"] ] = tmp
    i = i + 1

  return result


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Parse command line options.')
  parser.add_argument('args', nargs='*', help='list up github account e.g. hidenoly')
  parser.add_argument('-m', '--mode', action='store', default='dump', help='specify mode dump or clone')
  parser.add_argument('-l', '--filterLang', action='store', default='.*', help='specify language (regexp) if you want to filter')
  parser.add_argument('-r', '--filterRepo', action='store', default='.*', help='specify repository (regexp) if you want to filter')

  args = parser.parse_args()

  links = {}
  baseUrl = "https://github.com/"

  accounts = sys.argv
  del accounts[0]

  for anAccount in accounts:
    links = getLinks(baseUrl+anAccount+"?tab=repositories", links)

  for theText, theData in links.items():
    if re.match(args.filterLang, theData["lang"]) and re.match(args.filterRepo, theText):
      if args.mode == "dump":
        print('  "'+theText+'":{"url":"'+theData["url"]+'", "lang":"'+theData["lang"]+'"}",')
      elif args.mode == "clone":
        print("git clone "+theData["url"])
