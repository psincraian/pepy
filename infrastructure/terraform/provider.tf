provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "personal" {
  name = "personal"
}