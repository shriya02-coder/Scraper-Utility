@Override
public boolean saveOrUpdateTSProduct(TSProdAdminProductMappingDTO prodAdminProductMappingDTO) {
    // Log the entry into the method along with the incoming request details.
    logger.info("Entering saveOrUpdateTSProduct method in TSProdAdminServiceImpl");
    logger.info("Input parameter - prodAdminRequest: {}", AqueductUtil.getJsonStringFromObject(prodAdminProductMappingDTO));

    // Retrieve existing product entries based on the product code. This could potentially retrieve multiple entries (for "Fee" and "Balance").
    List<TSProdAdminVO> existingTSProducts = tsProdAdminImpl.getTSProdAdminVo(prodAdminProductMappingDTO.getProductCode());

    // Determine if this operation is an update based on if existing products are found.
    boolean isUpdate = !existingTSProducts.isEmpty();
    logger.info("isUpdate value: " + isUpdate);

    // Determine the types of spreads (liquidity default spreads) we need to handle based on the input.
    List<String> spreadTypes = new ArrayList<>();
    if ("Both".equalsIgnoreCase(prodAdminProductMappingDTO.getlLqdtyDefavltSpread())) {
        spreadTypes.add("Fee");
        spreadTypes.add("Balance");
    } else {
        spreadTypes.add(prodAdminProductMappingDTO.getlLqdtyDefavltSpread());
    }

    boolean anyUpdates = false; // Flag to track if any updates are made.

    // Process each spread type separately.
    for (String spreadType : spreadTypes) {
        // Check if an entry already exists for the specific spread type.
        TSProdAdminVO tsProdAdminVo = existingTSProducts.stream()
            .filter(product -> spreadType.equalsIgnoreCase(product.getLqdtyDefavltSpread()))
            .findFirst()
            .orElse(null);

        // If no existing product is found for the spread type, create a new one.
        if (tsProdAdminVo == null) {
            tsProdAdminVo = new TSProdAdminVO();
            tsProdAdminVo.setCreatedDt(new Date(System.currentTimeMillis()));
            tsProdAdminVo.setCreatedBy(prodAdminProductMappingDTO.getCreatedBy());
            logger.info("Creating a new product entry for spread type: {}", spreadType);
        } else {
            // If found, update the existing entry.
            tsProdAdminVo.setUpdateDt(new Date(System.currentTimeMillis()));
            tsProdAdminVo.setUpdateBy(prodAdminProductMappingDTO.getUpdatedBy());
            logger.info("Updating existing product entry for spread type: {}", spreadType);
        }

        // Set attributes for both new and updated cases.
        tsProdAdminVo.setProductCode(prodAdminProductMappingDTO.getProductCode());
        tsProdAdminVo.setWcrmProductId(String.valueOf(tsProductVO.getWcrmPrdId()));
        tsProdAdminVo.setFeeVsBalType(prodAdminProductMappingDTO.getFeeVsBalType());
        tsProdAdminVo.setVolType(prodAdminProductMappingDTO.getVolType());
        tsProdAdminVo.setMonthsToRamp(prodAdminProductMappingDTO.getMonthsToRamp());
        tsProdAdminVo.setMonthsToClose(prodAdminProductMappingDTO.getMonthsToClose());
        tsProdAdminVo.setLgdtyDefaultSpread(spreadType);
        tsProdAdminVo.setIsVisible(prodAdminProductMappingDTO.getIsVisible());

        // Save or update the product in the database.
        tsProdAdminImpl.saveOrUpdateTSProdAdmin(tsProdAdminVo);
        anyUpdates = true; // Mark that updates have been made.

        logger.info("Saved/Updated product details: {}", AqueductUtil.getJsonStringFromObject(tsProdAdminVo));
    }

    // After processing all types, if this was an update, perform audit comparisons.
    if (isUpdate) {
        compareAndAudit(existingTSProducts, prodAdminProductMappingDTO, prodAdminProductMappingDTO.getUpdatedBy());
    }

    // If the new spread type is not "Both" but previously was, remove the other entries.
    if (!"Both".equalsIgnoreCase(prodAdminProductMappingDTO.getlLqdtyDefavltSpread())) {
        existingTSProducts.stream()
            .filter(product -> !spreadTypes.contains(product.getLqdtyDefavltSpread()))
            .forEach(product -> {
                tsProdAdminImpl.deleteTSProdAdmin(product);
                logger.info("Deleted product entry for unused spread type: {}", product.getLqdtyDefavltSpread());
            });
    }

    logger.info("Product details saved/updated successfully");
    return anyUpdates; // Return whether any updates occurred.
}