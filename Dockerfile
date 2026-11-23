# Base image: Ruby with necessary dependencies for Jekyll
FROM ruby:3.2

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user with UID 1000
RUN groupadd -g 1000 vscode && \
    useradd -m -u 1000 -g vscode vscode && \
    install -d -o vscode -g vscode /opt/jekyll /usr/src/app

# Keep the Gemfile and Docker's lockfile outside the live source mount.
ENV BUNDLE_GEMFILE=/opt/jekyll/Gemfile
COPY --chown=vscode:vscode Gemfile /opt/jekyll/Gemfile

USER vscode
RUN bundle install

WORKDIR /usr/src/app
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--watch", "--force_polling", "--config", "_config.yml,_config_docker.yml"]

