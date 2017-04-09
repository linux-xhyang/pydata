
TEMP=/sys/class/projector/laser-projector
TEMP0=$TEMP/projector-0-temp/temp
TEMP1=$TEMP/projector-1-temp/temp
TEMP2=$TEMP/projector-2-temp/temp
TEMP3=$TEMP/projector-3-temp/temp

HEADER=date,temp0,temp1,temp2,temp3

FILE=/data/record-`date +%Y%m%d%H%M%S`.txt
function timestamp() {
    echo `date "+%Y-%m-%d %H:%M:%S"`
}

function get_temp() {
    case $1 in
        0)
            echo `cat $TEMP0`
            ;;
        1)
            echo `cat $TEMP1`
            ;;
        2)
            echo `cat $TEMP2`
            ;;
        3)
            echo `cat $TEMP3`
            ;;
        esac
}

echo $HEADER > $FILE
while [ true ];do
    echo -n $(timestamp), >> $FILE
    echo $(get_temp 0),$(get_temp 1),$(get_temp 2),$(get_temp 3) >> $FILE
    sleep 5
done
