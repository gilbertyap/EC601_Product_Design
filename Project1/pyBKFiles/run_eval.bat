set /p reference=Provide reference rttm file name in \out\ folder: 
set /p compare=Provide file name in \out\ folder to compare against reference: 
..\..\SharedResources\pyBK\eval-tools\md-eval-v21.pl -c 0.25 -s .\out\%compare%.rttm -r .\reference\%reference%.rttm
PAUSE