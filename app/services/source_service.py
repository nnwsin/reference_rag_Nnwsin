def build_sources(documents):
    sources = []
    seen_sources = set()

    for document in documents:
        filename = document.metadata.get(
            "filename",
            "unknown",
        )

        page = document.metadata.get("page")

        if page is not None:
            page = page + 1

        source_key = (filename, page)

        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)

        sources.append(
            {
                "filename": filename,
                "page": page,
            }
        )

    return sources