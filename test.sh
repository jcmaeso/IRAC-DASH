 echo ../Bento/bin/mp4encrypt --method MPEG-CENC --key 1:$2:random --property 1:KID:$3  --key 2:$2:random --property 2:KID:$3 --global-option mpeg-cenc.eme-pssh:true ./video/$1/frag_low.mp4 ./video/$1/enc_frag_low.mp4
 echo ../Bento/bin/mp4encrypt --method MPEG-CENC --key 1:$2:random --property 1:KID:$3 --global-option mpeg-cenc.eme-pssh:true ./video/$1/frag_medium.mp4 ./video/$1/enc_frag_medium.mp4
echo  ../Bento/bin/mp4encrypt --method MPEG-CENC --key 1:$2:random --property 1:KID:$3 --global-option mpeg-cenc.eme-pssh:true ./video/$1/frag_high.mp4 ./video/$1/enc_frag_high.mp4
