terraform {
  cloud {
    organization = "pepy"
    workspaces {
      tags = ["pepy"]
    }
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.22"
    }
  }
}