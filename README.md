# TestbeamTom

Macro for making a root file with histograms:
/nova/app/users/lasquith/tb_testrel/TestBeamAna/macros/examples/TomAnalysis1.C

You can copy this to your own TestBeamAna/macros/examples/ directory and run it like
cafe -bq -l 1 --tbana TomAnalysis1.C

Next you will want to run "on the grid" which will first require a test submission.

1. Make a tarball of your test release. For me this is:

cd /nova/app/users/lasquith/tb_testrel/

testrel_tarball . tb_tarball_1

where testrel_tarball is a command, the . meana "here", and tb_tabrall_1 is the name (can be anything) for your output tarball. Note that if the tarball tb_tarball_1.tar.bz2 already exists in the current directory, you will have to either delete it or make a new one with a different name, as testrel_tarball will not overwrite it.

2. Move the tarball somewhere sensible. For me this is:

mv tb_tarball_1.tar.bz2 /pnfs/nova/users/lasquith/scratch/testbeam/

you may have to make the directory with the mkdir command.

3. Do a test submission:

submit_cafana.py --test_submission --onsite_only -n 100 -r development -o /pnfs/nova/users/lasquith/scratch/testbeam/ --user_tarball /pnfs/nova/users/lasquith/scratch/testbeam/tb_tarball_1.tar.bz2 --tbana TestBeamAna/macros/examples/TomAnalysis1.C

Translation:
submit_cafana.py is the submission script
--test_submission ensures only three files are run on, as there will often be problems at this stage and you don't want to end up on the computing resources naughty list
--onsite_only not strictly necessary but I find it is more reliable
-n 100 split this submission up into 100 pieces
-r development this is the release you are working in
-o /pnfs/nova/users/lasquith/scratch/testbeam/ this is the output directory where your logfiles and histograms will be put. Note that when you run with --test_submission the outputs will go somewhere else, given in the output from your job submission. Make a note of that.
--user_tarball /pnfs/nova/users/lasquith/scratch/testbeam/tb_tarball_1.tar.bz2 is the path to your tarball
--tbana ensures that the libraries needed will be loaded
TestBeamAna/macros/examples/TomAnalysis1.C is the path to the macro you are running.

4. Check if the job has finished:

jobsub_q --user lasquith

5. Look in the output directory - for a test job this will be indicated by the job output prited to the terminal when you submit. If there is a root file in there you are all good. If there is not a root file there will still be a log file. Have a look in it to see what went wrong.

6. [if the job worked and you got a root file] Do a full submission:

submit_cafana.py --onsite_only -n 100 -r development -o /pnfs/nova/users/lasquith/scratch/testbeam/ --user_tarball /pnfs/nova/users/lasquith/scratch/testbeam/tb_tarball_1.tar.bz2 --tbana TestBeamAna/macros/examples/TomAnalysis1.C

(ie same as before but without the --test_submission flag)
Important note: if the output directory already has files named Period234-deltas.*_of_100.root, they will not be overwritten. The jobs will run but you will get no output.
This job might take an hour. Check the progress with
jobsub_q --user lasquith

If the grid refuses to work for you, you can still look at the following steps using the testfile I made, by not changing from lasquith to you in step 8

7. When the job has finished you will have 100 root files in your output directory. They will be named something like Period234-deltas.64_of_100.root You need to add them together like this:

cd /pnfs/nova/users/lasquith/scratch/testbeam/

hadd Period234-deltas.root Period234-deltas.*_of_100.root

where hadd is the command to add the files, Period234-deltas.root is the name you choose for the big combined file, and Period234-deltas.*_of_100.root has a wildcard * which is the same as listing all the 100 filename matching that pattern.

8. Copy the combined root file to your laptop:

scp lasquith@novagpvm02.fnal.gov:/pnfs/nova/users/lasquith/scratch/testbeam/Period234-deltas.root .

where scp is the command to securely copy,
lasquith@novagpvm02.fnal.gov:/pnfs/nova/users/lasquith/scratch/testbeam/Period234-deltas.root is the full path to the file you want to scp, including the login node lasquith@novagpvm02.fnal.gov
and the . at the end means "here"
Note that the first part of the path lasquith@novagpvm02.fnal.gov must be changed to your username, even if you are copying the file from my work area (and so will leave the second path with my username in it, /pnfs/nova/users/lasquith/scratch/testbeam/Period234-deltas.root

9. Run the attached python script to produce a set of plots.

python plot_vtx.py

Have a look at this script, you can use the pyroot guide I sent the other day to help figure out what is going on.

10. Edit and compile the attached latex beamer file to produce a set of slides with the plots in them.
I use TexShop for mac but I know you are windows so maybe Jess or Robert can help with that.
