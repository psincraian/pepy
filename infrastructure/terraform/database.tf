resource "digitalocean_droplet" "database" {
  image    = "ubuntu-20-04-x64"
  name     = "database"
  region   = var.region
  size     = "s-1vcpu-1gb"
  backups  = true
  ssh_keys = [data.digitalocean_ssh_key.terraform.id]
}

resource "digitalocean_volume" "db_volume" {
  name   = "db"
  region = var.region
  size   = 30
  initial_filesystem_type = "xfs"
}

resource "digitalocean_volume_attachment" "database_db_volume" {
  droplet_id = digitalocean_droplet.database.id
  volume_id  = digitalocean_volume.db_volume.id
}