set /p reference=Provide reference rttm file name in \pyBKFiles\reference\ folder: 
set /p compare=Provide file name in \pyBKFiles\out\ folder to compare against reference: 
..\SharedResources\pyBK\eval-tools\md-eval-v21.pl -c 0.25 -s .\pyBKFiles\out\%compare%.rttm -r .\pyBKFiles\reference\%reference%.rttm
PAUSE