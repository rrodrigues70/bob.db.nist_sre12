Speaker recognition protocol on the NIST SRE 2012 Database 
==========================================================

The `2012 NIST Speaker Recognition Evaluation`_ (SRE12) is part of an ongoing series that starts in 1996.

In this package, we implement speaker recognition protocols (both Male and Female) for the NIST SRE 2012.
The file lists of the development set were designed by the I4U consortium during its participation to the competition.
Special thanks to Rahim Saeidi (original link of the lists: http://cls.ru.nl/~saeidi/file_library/I4U.tgz).
The file names were then normalized following the `PRISM definition`_.

This package is automatically downloaded/used by `spear.nist_sre12`_ to reproduce the results of Idiap Research Institute at SRE12.
`spear.nist_sre12`_ itself relies on `spear`_, an open-source speaker recognition toolbox developed at Idiap.
The list files can also be used independently as explained below.

If you use this package and/or its results, please cite the following publications:

1. The Spear paper published at ICASSP 2014::

    @inproceedings{spear,
      author = {Khoury, E. and El Shafey, L. and Marcel, S.},
      title = {Spear: An open source toolbox for speaker recognition based on {B}ob},
      booktitle = {IEEE Intl. Conf. on Acoustics, Speech and Signal Processing (ICASSP)},
      year = {2014},
      url = {http://publications.idiap.ch/downloads/papers/2014/Khoury_ICASSP_2014.pdf},
    }


2. The paper that described the development set used by the I4U consortium::

    @inproceedings{Saedi_INTERSPEECH_2013,
       author = {Saeidi, Rahim and others},
       month = {aug},
       title = {I4U Submission to NIST SRE 2012: a large-scale collaborative effort for noise-robust speaker verification},
       booktitle = {INTERSPEECH},
       year = {2013},
       location = {Lyon, France},
       pdf = {http://publications.idiap.ch/downloads/papers/2013/Saedi_INTERSPEECH_2013.pdf}
    }


3. Bob as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos and L. El Shafey and R. Wallace and M. G\"unther and C. McCool and S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = {oct},
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }



Installation
------------

Just download this package and decompress it locally::

  $ wget http://pypi.python.org/packages/source/x/xbob.db.nist_sre12/xbob.db.nist_sre12-1.1.1.zip
  $ unzip xbob.db.nist_sre12-1.1.1.zip
  $ cd xbob.db.nist_sre12-1.1.1

Use buildout to bootstrap and have a working environment ready for experiments::

  $ python bootstrap
  $ ./bin/buildout

This also requires that bob (>= 1.2.0) is installed.

To create the SQL database, just run the following command line (this can take 6-7 minutes)::
  
  $ bin/bob_dbmanage.py nist_sre12 create

Getting the data
~~~~~~~~~~~~~~~~

You need to order the NIST SRE databases (Fisher, Switchboard, and Mixer)::

  http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03

Please follow the instructions and the evaluation plan given by NIST::

  http://www.nist.gov/itl/iad/mig/sre12.cfm

Depending on the release year, the data may need to be flatten and reorganized.
Please, follow the file structure as appearing when running::
 
  $ bin/bob_dbmanage.py nist_sre12 dumplist

For this purpose, you will need the utilities provided by NIST with the database, as well as `sox`.

.. _sox: http://sox.sourceforge.net/


Decompressing the data and splitting the audio channels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The data provided by NIST are compressed in a non-standard format.
NIST supplies a binary called `w_decode` to perform the decompression.
Therefore, you should decompress all the files using the following command (where NIST_FOLDER/bin is the one containing the `w_decode` utility::

  $ NIST_FOLDER/bin/w_decode -o pcm $compressedfile $decompressedfile

Several files are in stereo and hence contain two audio channels.
These files needs to be split using a script similar to the following one::

  $ decompressedfileStereo=`basename $decompressedfile .sph`
  $ num=`soxi $decompressedfile | grep Channels | cut -c 18`
  $ echo $num
  $ if [ $num -eq 2 ]
  $ then # File is stereo
  $   echo sox $decompressedfile -c 1 $outputDir/${decompressedfileStereo}-a.sph mixer -l
  $   sox $decompressedfile -c 1 $outputDir/${decompressedfileStereo}-a.sph mixer -l
  $   sox $decompressedfile -c 1 $outputDir/${decompressedfileStereo}-b.sph mixer -r
  $ else # File is mono
  $   echo cp $decompressedfile $outputDir/
  $   cp $decompressedfile $outputDir/
  $ fi

   
Adding noise
~~~~~~~~~~~~

In order to better represent the SRE12 evaluation set, 2 noisy versions (SNR=6dB and SNR=15dB) of the same segments were included to the development set (both target models and test utterances).
This can be done using FaNT::
  
  http://dnt.kr.hsnr.de/download.html

The noise samples were mainly collected from freesound.org and include HVAC and crowd noise. They are available under request. The description of the added noise for each of the audio files can be found here::

 $ cd xbob/db/nist_sre12/noise_description/
 

Speech enhancement
~~~~~~~~~~~~~~~~~~

The denoising of the audio signal can be done using QIO::
  
  http://www1.icsi.berkeley.edu/Speech/papers/qio/

.. _nist_sre12: http://www.nist_sre12.org/
.. _spear: https://github.com/bioidiap/bob.spear
.. _spear.nist_sre12: https://github.com/bioidiap/spear.nist_sre12
.. _2012 NIST Speaker Recognition Evaluation: http://www.nist.gov/itl/iad/mig/sre12.cfm
.. _PRISM definition: http://code.google.com/p/prism-set


Using independently the file lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The file lists of the development and evaluation sets are shipped with this package.
They can be used independently, and can be found here::

  $ cd xbob/db/nist_sre12/prism/

The file lists of the development set were prepared by the I4U consortium.

In case you need any help, please contact us.
