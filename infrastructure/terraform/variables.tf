variable "do_token" { description = "DigitalOcean token" }
variable "ssh_private_key" { description = "Private ssh key used to access droplets to provision them" }
variable "region" {
  description = "Region where to deploy infrastructure"
  default     = "nyc1"
}
