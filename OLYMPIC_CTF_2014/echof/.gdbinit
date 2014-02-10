
b *(main+519)

b *(main+592)
commands
silent
p "cookie"
i r edx
c
end

b *(main+607)
commands
silent
p "return"
x /wx $esp
end
