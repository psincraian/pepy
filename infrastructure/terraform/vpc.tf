resource "digitalocean_vpc" "pepy-vpc" {
  name     = "pepy-vpc"
  region   = var.region
  ip_range = "10.0.0.0/24"
}