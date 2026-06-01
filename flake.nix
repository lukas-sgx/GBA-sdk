{nixpkgs, ...}:

nixpkgs.mkShell = {
  packages = [
    devenv
  ];

  shellHook = ''
    devenv shell
  ''  
}
