# Sonatype Nexus Provider
[Sonatype Nexus Website](https://www.sonatype.com/products/nexus-repository)

Based on the [nexus terraform provider](https://github.com/datadrivers/terraform-provider-nexus) by datadrivers.

&nbsp;

The Nexus resource provider for Pulumi lets you use and manage Sonatype Nexus resources in your Infrastructure as Code deployments.


## Installing

This package is available in C#, TypeScript, Python and Go

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Nexus
```

### Node.js (Java/TypeScript)

```bash
npm install @simcubeltd/pulumi-nexus
```

or `yarn`:

```bash
yarn add @simcubeltd/pulumi-nexus
```

### Python

To use from Python, install using `pip`:

```bash
pip install simcubeltd_pulumi_nexus
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/SimCubeLtd/pulumi-nexus/sdk/go/nexus
```

## Configuration

The following configuration entries are available:

| **Key**           | **Value**                                                  |
|-------------------|:-----------------------------------------------------------|
| nexus:insecure    | Boolean, true if http, false if https.                     |
| nexus:url         | Url to the nexus instance, including relevant port.        |
| nexus:username    | Account Username for Nexus (account must have admin role). |
| nexus:password    | Account password for Nexus (account must have admin role). |
