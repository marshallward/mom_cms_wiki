#!/usr/bin/env python
"""
mw2wt.py
Mediawiki to Wikitext translator
Patch the mediawiki output to match the format in UNSW's wiki
Contact: Marshall Ward (marshall.ward@gmail.com)
"""
import sys
import re

wiki_fname = sys.argv[1]
f_old = open(wiki_fname, 'r')
f_new = open(wiki_fname + '~', 'w')

for line in f_old:
    # Fix monospace
    line = line.replace('<tt>', '{{')
    line = line.replace('</tt>', '}}')
    
    # Fix bold
    line = line.replace("'''", "**")
    
    # Fix coding
    pattern = '<source lang="(.+?)">'
    match = re.search(pattern, line)
    if match:
        src_lang = match.group()
        lang = match.groups()[0]
        
        code_lang = lang.join(['[[code format="', '"]]\n'])
        line = line.replace(src_lang, code_lang)

    line = line.replace('</source>', '\n[[code]]\n')
    
    # Fix links
    link_patterns = ['\[http(.+?)\]', '\[mailto(.+?)\]']
    for pattern in link_patterns:
        match = re.search(pattern, line)
        if match:
            old_link = match.group()
            new_link = '[' + '|'.join(old_link.split(' ', 1)) + ']'
            line = line.replace(old_link, new_link)
    
    f_new.write(line)

f_old.close()
f_new.close()
