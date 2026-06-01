{ pkgs ? import <nixpkgs> { } }:
with pkgs;
pkgs.mkShell {
  packages = [
    pkgs.devenv
  ];

  shellHook = ''
    devenv shell
  '';
};