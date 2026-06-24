{ pkgs, ... }:

{
  env.GREET = "devenv";

  packages = [
    pkgs.libxkbcommon
    pkgs.vulkan-loader
    pkgs.wayland
    pkgs.gcc-arm-embedded-13
    pkgs.cmake
  ];
  
  languages.python = {
    enable = true;
    venv.enable = true;
  };

  enterShell = ''
    pip install -e "." --quiet
    git --version # Use packages
  '';
  
  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.libxkbcommon
    pkgs.vulkan-loader
    pkgs.wayland
    pkgs.libxkbcommon
  ];

  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';
}
