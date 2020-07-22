//msg.topic = "ph"; 
var y = msg.payload;
var x= parseFloat(y);

if (6.8 < x  && x < 7.6)
{
    msg.payload = "Normal";
    return msg;
}
else if (x < 6.8)
{
    msg.payload = "Acidic";
    return msg;
}
else (x >7.6)
{
    msg.payload ="Basic";
    return msg;
}
