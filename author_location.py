#!/usr/bin/env python3
#
# This script takes a single PubMed ID and hits the eutils URL
# to get the affiliation of the last author and writes it to stdout
#
# In practice, it's probably a good idea if you are planning on hitting
# eutils for several PMIDs to do it in a shell script with a sleep of
# at least a few seconds between requests.
#
import sys
import requests
import xml.etree.ElementTree as ET

def get_last_author_affiliation(pubmed_id):
    """Fetch PubMed article and return last author's affiliation."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        # Find all authors
        authors = root.findall(".//Author")
        
        if not authors:
            return "No authors found"
        
        # Get the last author
        last_author = authors[-1]
        
        # Try to find affiliation
        affiliation = last_author.find(".//Affiliation")
        
        if affiliation is not None and affiliation.text:
            # Get author name for context
            last_name = last_author.find("LastName")
            fore_name = last_author.find("ForeName")
            
            name = ""
            if last_name is not None:
                name = last_name.text
            if fore_name is not None:
                name = f"{fore_name.text} {name}"
            
            return f"{affiliation.text}"
            
    except requests.RequestException as e:
        return f"Error fetching data: {e}"
    except ET.ParseError as e:
        return f"Error parsing XML: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <PubMed_ID>")
        sys.exit(1)
    
    pubmed_id = sys.argv[1]
    result = get_last_author_affiliation(pubmed_id)
    print(result)
