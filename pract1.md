task1: 
```
#!/bin/bash
grep -o ‘^[^:]*’ /etc/passwd | sort
```

task2: 
```
cat /etc/protocols | sort -rnk2 | head -n 5 | awk ‘{print $2, $1}’
```

task3:
```
textOfFrame="$1"
lenOfFrame=$(($(wc -c <<< "$textOfFrame")+1))

print_border() {
	printf "+"

	for((i=0; i<"$lenOfFrame"; i++)); do
		printf "-"
	done

	printf "+\n"
}

print_border
printf "| %s |\n" "$textOfFrame"
print_border
```

task4:
```
cat a.cpp | grep -o “[A-Za-z][A-Za-z0-9_$]*” | sort | uniq
```

task5:
```
chmod +x “$1” 
sudo cp “$1” /usr/local/bin
```

task6:
```
shopt -s nullglob globstar

for file in **/*.{c,js,py}; do
	firstLine="$(head -n 1 "$file")"

	# Python comment
	if [[ "$file" == *.py ]]; then
		if grep -q '^#' <<< "$firstLine"; then
			echo "$file"
		fi
	# .c comment
	elif [[ "$file" == *.c ]]; then
		if grep -qE '^(//|/\*)' <<< "$firstLine"; then
			echo "$file"
		fi
	# .js comment
	elif [[ "$file" == *.js ]]; then
                if grep -qE '^(//|/\*)' <<< "$firstLine"; then
                        echo "$file"
                fi
	fi

done
```

task7:
```
shopt -s nullglob globstar

for i in **/*; do
	if [ -f "$i" ]; then
		md5sum "$i";
	fi
done | sort | uniq -w32 -D | tr -s ' ' | cut -d' ' -f2
```

task8:
```
tar -cf  “ArchiveTest1.tar” *”$1”
```

task9:
```
sed 's/    /\t/g' < "$1" > "$2"
```

task10:
```
for file in "$1"/*; do
	if [ ! -s "$file" ] && grep -qEi "\.(docx|doc|txt)$" <<< "$file"; then 
		printf '%s\n' "$file"
	fi
done
```

