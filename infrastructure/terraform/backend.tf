resource "digitalocean_droplet" "backend" {
  image    = "ubuntu-20-04-x64"
  name     = "backend"
  region   = var.region
  size     = "s-1vcpu-512mb-10gb"
  ssh_keys = [data.digitalocean_ssh_key.terraform.id]
}