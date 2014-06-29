IP=$(cat ip.txt)
echo $IP
ssh $IP "
cp /data/data/com.android.providers.telephony/databases/mmssms.db /sdcard/
exit
"
scp $IP:/sdcard/mmssms.db databases/
chmod 666 databases/mmssms.db