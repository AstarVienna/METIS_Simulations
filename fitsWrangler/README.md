
## FITSWrangler

Routines for generating empty test files, or reformatting data into METIS pipeline compatible routines. The idea is to be able to decouple fiddling with details of the format from the code that generates the data. Some input sources, like ScopeSim, may have fairly complete header keywords while others may not; this interface will either copy over header information, add new header information, or both. In addition, it's designed so that we can add new formats or keywords easily, without changing the API. 

This cake be used to

 - generate a minimal FITS file with data set to zero, with
   appropriate extentions and header keywords for input METIS pipleline recipes

or

 - take input data from a variety of sources, and output FITS files suitable for
   use in testing METIS pipeline recipes.

The latter can be done in several was

 - take ScopeSim output, copy the data and headers over unchanged, add
   METIS extension and HDUClass headers and write to file. 

 - do the same, but add or delete keywords as needed

 - take data from other sources, or ScopeSim output that has been post
   processed, or a combination, copy the data into the appropriate
   exensions and create the FITS file.


The FITS creation routines take two parameters, a file name, and a
structure containing data / headers / keywords.  This structure can be
initialized by calling

    parms = makeBasicParameters(format,instrument)

where the current options are

 - Format = raw, processed

 - instrument = lm, n, lss, ifu, ifu_cube, lss_spectrum


### Format of Parameter Structure

    parms['instrument']  # what instrument
    parms['defaultSize'] # default shape of the data numpy array

    parms['primary']['header'] # primary header (or None)
    parms['primary']['keywords'] # dictionary of keywords and values to add to the header

For the following i = 0 for L/M/LSS and 0,1,2,3 for IFU
 
    parms['data'][i]['data'] # numpy array, or None
    parms['data'][i]['header'] # FITS header, or None
    parms['data'][i]['keywords'] # dictionary of keywords and values, or None
    
If the output is for processed data, the above three items are repeated for the quality and error extensions

    parms['error'][i]
    parms['quality'][i]
    
See the notebook examples.ipynb for how to call the routines and alter the paramter structure. 



