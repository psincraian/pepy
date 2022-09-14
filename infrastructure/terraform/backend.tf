resource "digitalocean_droplet" "backend" {
  image    = "ubuntu-20-04-x64"
  name     = "backend"
  region   = var.region
  size     = "s-1vcpu-512mb-10gb"
  ssh_keys = [data.digitalocean_ssh_key.terraform.id]

  provisioner "local-exec" {
    command = <<EOT
      "sudo apt-get install ansible -y"
      "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root -i '${self.ipv4_address},' --private-key ${var.ssh_private_key} provision-web.yml"
    EOT
  }
}