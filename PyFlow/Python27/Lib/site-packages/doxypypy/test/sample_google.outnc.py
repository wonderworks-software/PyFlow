#!/usr/bin/env python
## @brief Google Python Style Guide SampleClass
#
#This is basically as close a copy of the Python examples in the Google
#Python Style Guide as possible while still being valid code.
#
#http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments
#



## @brief Fetches rows from a Bigtable.
#
#    Retrieves rows pertaining to the given keys from the Table instance
#    represented by big_table.  Silly things may happen if
#    other_silly_variable is not None.
#
#
# @param		big_table	An open Bigtable Table instance.
# @param		keys	A sequence of strings representing the key of each table row
#            to fetch.
# @param		other_silly_variable	Another optional variable, that has a much
#            longer name than the other args, and which does nothing.
#
# @return
#        A dict mapping keys to the corresponding table row data
#        fetched. Each row is represented as a tuple of strings. For
#        example:
#
#        {'Serak': ('Rigel VII', 'Preparer'),
#         'Zim': ('Irk', 'Invader'),
#         'Lrrr': ('Omicron Persei 8', 'Emperor')}
#
#        If a key from the keys argument is missing from the dictionary,
#        then that row was not found in the table.
#
#
# @exception		IOError	An error occurred accessing the bigtable.Table object.
#
# @namespace sample_google.fetch_bigtable_rows
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    pass


## @brief Summary of class here.
#
#    Longer class information....
#    Longer class information....
#
#
#
# @namespace sample_google.SampleClass
class SampleClass(object):

    ## @property		likes_spam
    # A boolean indicating if we like SPAM or not.

    ## @property		eggs
    # An integer count of the eggs we have laid.

    ## @brief Inits SampleClass with blah.
    # @namespace sample_google.SampleClass.__init__
    def __init__(self, likes_spam=False):
        self.likes_spam = likes_spam
        self.eggs = 0

    ## @brief Performs operation blah.
    # @namespace sample_google.SampleClass.public_method
    def public_method(self):
        pass

i = None

# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:        # true iff i is a power of 2
    pass
