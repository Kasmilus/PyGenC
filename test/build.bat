@echo off
set CommonCompilerFlags=-Od -nologo -FC -WX -W4 -wd4201 -wd4100 -wd4505 -wd4189 -wd4457 -wd4456 -wd4819 -MTd -Oi -GR- -Gm- -EHa- -Zi
set CommonLinkerFlags=-incremental:no -opt:ref

REM Optimization switches: /O2 /Oi /fp:fast
cl %CommonCompilerFlags% main.c -LD /link %CommonLinkerFlags% /out:test.dll

del *.pdb > NUL 2> NUL
del *.obj > NUL 2> NUL
del *.lib > NUL 2> NUL
del *.exp > NUL 2> NUL
