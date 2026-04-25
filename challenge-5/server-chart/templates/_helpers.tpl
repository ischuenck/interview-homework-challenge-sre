{{- define "server-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "server-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "server-chart.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "server-chart.labels" -}}
app.kubernetes.io/name: {{ include "server-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}

{{- define "server-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "server-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
