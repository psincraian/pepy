resource "digitalocean_droplet" "database" {
  image    = "ubuntu-20-04-x64"
  name     = "database"
  region   = var.region
  size     = "s-1vcpu-1gb"
  backups  = true
  ssh_keys = [data.digitalocean_ssh_key.terraform.id]
  vpc_uuid = digitalocean_vpc.pepy-vpc.id
}

resource "digitalocean_volume" "db_volume" {
  name                    = "db"
  region                  = var.region
  size                    = 30
  initial_filesystem_type = "xfs"
}

resource "digitalocean_volume_attachment" "database_db_volume" {
  droplet_id = digitalocean_droplet.database.id
  volume_id  = digitalocean_volume.db_volume.id
}

resource "digitalocean_firewall" "database_firewall" {
  name = "mongodb-open-vpc"

  droplet_ids = [digitalocean_droplet.database.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "27017"
    source_addresses = ["10.0.0.0/24"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}