var y = msg.payload;
var x= parseFloat(y);
if (20 < x  && x < 30)
{
    msg.payload = "Normal";
    return msg;
}
else if (x < 20)
{
    msg.payload = "Low";
    return msg;
}
else (x >30)
{
    msg.payload ="High";
    return msg;
}