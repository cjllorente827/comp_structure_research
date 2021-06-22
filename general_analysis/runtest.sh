#!/bin/bash

touch ytProjMemTest.md
rm ytProjMemTest.md

echo "# Results of testing the projection plot memory usage" >> ytProjMemTest.md
for test in 1 2 3 4 5
do 
echo "# Test ${test}" >> ytProjMemTest.md
echo "" >> ytProjMemTest.md
    for frames in 1 10 300   
    do 
        echo "" >> ytProjMemTest.md
        echo "## Creating ${frames} frame(s) from dataset" >> ytProjMemTest.md
        echo "" >> ytProjMemTest.md
        echo "\`\`\`" >> ytProjMemTest.md

        python test.py ${test} ${frames} >> ytProjMemTest.md

        echo "\`\`\`" >> ytProjMemTest.md
    done
done

echo "All done!"