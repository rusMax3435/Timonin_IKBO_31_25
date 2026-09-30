task1: 
grep -o ‘^[^:]*’ /etc/passwd | sort

task2: 
cat /etc/protocols | sort -rnk2 | head -n 5 | awk ‘{print $1, $2}’

task4: 
cat a.cpp | grep -o “[A-Za-z][A-Za-z0-9_$]*” | sort | uniq

task5: 
chmod +x “$1” 
sudo cp “$1” /usr/local/bin

task8: 
Tar -cf  “ArchiveTest1.tar” *”$1”
