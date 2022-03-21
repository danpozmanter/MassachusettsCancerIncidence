cd data
echo "Processing raw data..."
python process_raw.py
echo "Generating JSON and additional data for static site..."
python generate_city_data.py
cd ..
cp data/cities.json site/
cp data/ranked_city_data/* site/data/
echo "Generated data has been copied over."