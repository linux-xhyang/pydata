
TEMP=/sys/class/projector/laser-projector
TEMP0=$TEMP/projector-0-temp/temp
TEMP1=$TEMP/projector-1-temp/temp
TEMP2=$TEMP/projector-2-temp/temp
TEMP3=$TEMP/projector-3-temp/temp
FAN1=$TEMP/fan1_control
FAN2=$TEMP/fan1_control
FAN3=$TEMP/fan1_control

HEADER=date,fan1,fan2,fan3,temp0,temp1,temp2,temp3

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

function get_fan() {
    case $1 in
        0)
            echo `cat $FAN1`
            ;;
        1)
            echo `cat $FAN2`
            ;;
        2)
            echo `cat $FAN3`
            ;;
    esac
}

echo $HEADER > $FILE
while [ true ];do
    echo -n $(timestamp), >> $FILE
    echo $(get_fan 0),$(get_fan 1),$(get_fan 2),$(get_temp 0),$(get_temp 1),$(get_temp 2),$(get_temp 3) >> $FILE
    sleep 2
done
