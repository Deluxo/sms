IP=$(cat ip.txt)
echo $IP
scp databases/mmssms.db $IP:/sdcard/ 
ssh $IP "
cp /sdcard/mmssms.db /data/data/com.android.providers.telephony/databases/
exit
"
chmod 666 databases/mmssms.db