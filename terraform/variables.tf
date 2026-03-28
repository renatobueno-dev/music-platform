variable "kubeconfig_path" {
  type        = string
  description = "Path to the kubeconfig file used by the Kubernetes provider."
  default     = "~/.kube/config"

  validation {
    condition     = length(trimspace(var.kubeconfig_path)) > 0
    error_message = "kubeconfig_path must be a non-empty path."
  }
}

variable "namespace_name" {
  type        = string
  description = "Namespace managed as Terraform baseline."
  default     = "music-platform"

  validation {
    condition = (
      length(var.namespace_name) <= 63
      && can(regex("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", var.namespace_name))
    )
    error_message = "namespace_name must be a valid RFC 1123 DNS label (lowercase alphanumeric or '-', max 63 chars)."
  }
}

variable "namespace_labels" {
  type        = map(string)
  description = "Optional custom labels for the managed namespace."
  default     = {}
}

variable "namespace_annotations" {
  type        = map(string)
  description = "Optional custom annotations for the managed namespace."
  default     = {}
}

variable "pod_security_level" {
  type        = string
  description = "Pod Security Standards level applied to namespace labels."
  default     = "restricted"

  validation {
    condition     = contains(["privileged", "baseline", "restricted"], var.pod_security_level)
    error_message = "pod_security_level must be one of: privileged, baseline, restricted."
  }
}

variable "pod_security_version" {
  type        = string
  description = "Pod Security Standards version for namespace labels."
  default     = "latest"

  validation {
    condition     = length(trimspace(var.pod_security_version)) > 0
    error_message = "pod_security_version must be non-empty (for example: latest or v1.30)."
  }
}
