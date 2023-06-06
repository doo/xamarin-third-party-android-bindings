API_KEY=$1

if [ -z "$API_KEY" ]; then
    echo "Please specify an api key"
    exit 1;
fi

PACKAGES=$(find nuget-dist/Scanbot.NET.*)

echo
echo "Found packages:"
echo
for i in $PACKAGES; do
    echo "$i"
done
echo

read -p "Are you sure you want to publish these packages(y/n)? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]; then
    for i in $PACKAGES; do
        echo
        echo "Uploading package $i"
        echo
        nuget push $i -ApiKey $API_KEY -Timeout 600 -Source nuget.org
    done  
fi