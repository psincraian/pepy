resource "digitalocean_project" "pepy" {
  name        = "pepy"
  description = "pepy.tech production infrastructure"
  purpose     = "Web Application"
  environment = "Production"
  resources   = [digitalocean_droplet.database.urn, digitalocean_droplet.backend.urn, digitalocean_volume.db_volume.urn]
}