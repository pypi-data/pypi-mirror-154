#TBSE Documentation
*Grammar*
*Escape characters:*
```
#a -> &
#q -> '
## -> #
#. -> blank
#x** -> character from hex **
#u**** -> character from unicode ****
```
*Commands:*
```
alias:make an alias, or search in the list
{alias}
{alias <a>}
{alias <a>=<b>}
busybox:execute busybox command
{busybox <command>}
{busybox --on}\033[90m#type exit to exit\033[0m
clearqq:remove qq cache
{clearqq}
do:open do editor
{do}
echo:print strings
{echo <content>}
exit:exit this program
{exit [code]}
help:get helps
{help}
home:set home dir
{home <dir>}
input:make a break
{input}
int/str/bln:define a variable
{<int|str|bln> <variable_name>}
raise:make an error in tool.py
{raise [error]}
ps:toggle ps
{ps [ps_name]}
run:execute a file like *.tb
{run <-p|*.tb>}
sdb:like sdebr
{sdb conn <host:port>}
{sdb on <rand|host:port>}
{sdb off conn}
set:set a value to a variable
{set <variable_name>=<value>}
{set -p <variable_name>}
sh:execute shell command
{sh <command>}
{sh --on}\033[90m#type exit to exit\033[0m
uninstall:uninstall some programs and packages
{uninstall}
update:information for updates
{update}
ver:version
{ver}
wait:make the program pause
{wait <time/ms>}
```

count of views:
![count of views](https://count.getloli.com/get/@tbse)
