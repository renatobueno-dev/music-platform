terraform {
  backend "kubernetes" {
    namespace     = "kube-system"
    secret_suffix = "music-platform"
  }
}
