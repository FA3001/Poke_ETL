# Install Astro CLI if not already installed
if ! command -v astro &> /dev/null
then
    echo "🔧 Installing Astro CLI..."
    curl -sSL install.astronomer.io | sudo bash -s
else
    echo "✅ Astro CLI already installed."
fi

# Install project dependencies
echo "📦 Installing project dependencies..."
astro dev install

# Start Astro project
echo "🚀 Starting Astro project..."
astro dev start

echo "✅ Astro project is now running!"
echo "👉 Airflow UI: http://localhost:8080"