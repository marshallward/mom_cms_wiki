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

# Basic substitutions (mostly HTML to wikitext)
subs = {'&amp;':        '&',
        '&quot;':       '"',
        "'''":          '**',   # Bold (emphasis)
        '<tt>':         '{{',
        '</tt>':        '}}',
        '<source>':     '[[code]]\n',
        '</source>':    '\n[[code]]'
        }

for line in f_old:
    #--------------------------------------------
    # Blank line detection (for code blocks)
    if line == '\n':
        prior_line = line
        try:
            line = f_old.next()
        # Break for end-of-file exception
        except StopIteration:
            f_new.write(prior_line)
            break
    else:
        prior_line = None
    
    # Basic substitutions
    for s in subs:
        line = line.replace(s, subs[s])
    
    #-----------
    # Fix links
    protocols = ['http', 'mailto', 'ftp']
    link_patterns = ['\[' + s + '(.+?)\]' for s in protocols]
    for pattern in link_patterns:
        match = re.search(pattern, line)
        if match:
            old_link = match.group()
            new_link = '[' + '|'.join(old_link.split(' ', 1)) + ']'
            line = line.replace(old_link, new_link)
    
    #-----------------
    # Fix code blocks
    pattern = '<source lang="(.+?)">'
    match = re.search(pattern, line)
    if match:
        src_lang = match.group()
        lang = match.groups()[0]
        
        code_lang = lang.join(['[[code format="', '"]]\n'])
        line = line.replace(src_lang, code_lang)
    elif prior_line:
        f_new.write(prior_line)
    
    f_new.write(line)

f_old.close()
f_new.close()
