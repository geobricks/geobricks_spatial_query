sudo -u postgres createuser --superuser spatialuser
sudo -u postgres psql
\password spatialuser
#insert password (spatial)
#\q
createdb -U spatialuser spatialdbtest
psql -U spatialuser -d spatialdbtest -c "CREATE EXTENSION postgis;"
shp2pgsql -W LATIN1 -I -s 4326 ne_110m_admin_0_countries.shp spatial.ne_110m_admin_0_countries | psql -U spatialuser spatialdbtest
