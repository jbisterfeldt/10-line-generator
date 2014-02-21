from fdfgen import forge_fdf
import random
import os
import subprocess

# Generate a set of random 10 line raffle cards, 6 per page
# Optionally output as a single pdf
# Requires fdfgen module and pdftk

# Usage: output_cards(100)
# Generates 100 pages (600 cards)

# Also known as:
# Add 'em up, 10-line, #10, 10-strip, football cards, sports cards

def gen_card(cardname):
    '''Generate fields for one card. Returns list of two-tuple name,value.'''
    nums = [0,1,2,3,4,5,6,7,8,9]
    random.shuffle(nums)
    card_fields = [(cardname+', Win',random.choice(nums)),
              (cardname+', Slot 1',str(nums.pop())),
              (cardname+', Slot 2',str(nums.pop())),
              (cardname+', Slot 3',str(nums.pop())),
              (cardname+', Slot 4',str(nums.pop())),
              (cardname+', Slot 5',str(nums.pop())),
              (cardname+', Slot 6',str(nums.pop())),
              (cardname+', Slot 7',str(nums.pop())),
              (cardname+', Slot 8',str(nums.pop())),
              (cardname+', Slot 9',str(nums.pop())),
              (cardname+', Slot 10',str(nums.pop()))]
    return card_fields

def gen_fdf(outfile='data.fdf'):
    '''Generate random numbers to form fill 10-liner cards, save FDF file.'''
    fields = []
    increment = 0
    for card in range(6):
        increment += 1
        cardname = 'Card '+str(increment)
        fields += gen_card(cardname)
    fdf = forge_fdf("",fields,[],[],[])
    fdf_file = open(outfile,"w")
    fdf_file.write(fdf)
    fdf_file.close()

def fill_and_flatten(infile,datafile,outfile):
    flatten = ('pdftk '+infile+' fill_form '+datafile+' output '+outfile+' flatten')
    os.system(flatten)

def cat_all_pdf():
    command = 'pdftk *.pdf cat output final.pdf'
    subprocess.call(command)

def output_cards(num_output=10,onefile=True,cleanup=True):
    for i in range(num_output):
        print('Processing page #'+str(i+1))
        gen_fdf()
        filename = 'temp'+str(i)+'.pdf'
        layoutpath = os.path.join('resources','layout.pdf')
        fill_and_flatten(layoutpath,'data.fdf',filename)
    if onefile:
        print('Merging output into final.pdf:')
        cat_all_pdf()
    if cleanup:
        print('Cleaning up temporary files.')
        os.remove('data.fdf')
        for i in range(num_output):
            filename = 'temp'+str(i)+'.pdf'
            if os.path.isfile(filename):
                os.remove(filename)
    print('Done.')

output_cards(int(raw_input('Enter number of pages to output: ')))
 
