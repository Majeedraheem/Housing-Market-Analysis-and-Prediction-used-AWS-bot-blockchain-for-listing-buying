pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract payForProperty{
    uint public accountBalance;
    
    function sendPayment(address payable to, address from, uint256 amount) public {
        require(from == msg.sender, "Only the buyer sends coins");
        to.transfer(amount);
        accountBalance = address(this).balance;
    }

    function deposit() public payable {
        accountBalance = address(this).balance;
    }

    function () external payable {}
}

contract PropertyRegistry is ERC721Full, payForProperty {
    constructor() public ERC721Full("PropertyRegistryToken", "HOME") {}

    address payable contractAddress = address(uint160(address(this)));
    uint public collectionSize = 0;

    struct Property {
        address owner;
        string geoAddress;
        string propType;
        uint256 appraisalValue;
        string propJson;
    }

    // propCollection will act as a 'dictionary' of all Property (value), and their tokenId (key)
    mapping(uint256 => Property) public propCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI, string propJson);
    
    function imageUri(
        uint256 tokenId
    ) public view returns (string memory propJson){
        return propCollection[tokenId].propJson;
    }

    function registerProperty(
        address payable owner,
        string memory geoAddress,
        string memory propType,
        uint256 initialAppraisalValue,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        setApprovalForAll(contractAddress, true);

        _setTokenURI(tokenId, tokenURI);

        propCollection[tokenId] = Property(owner, geoAddress, propType, initialAppraisalValue, tokenJSON);
        collectionSize++;

        return tokenId;
    }

    // When buying a property in ERC721, the token must be transfered to the buyer.
    // The amount of currency to be exchanged must be done outside the ERC721 contract.
    function buyProperty(uint256 token_id) public {
        // The buyer is the caller and we must ensure that the seller's address is payable
        address buyer_address = msg.sender;
        address payable seller_address = address(uint160(ownerOf(token_id)));
        uint256 amount = propCollection[token_id].appraisalValue;

        require(buyer_address != seller_address, "Sellers cannot buy their own property");

        sendPayment(seller_address, buyer_address, amount);
        safeTransferFrom(seller_address, buyer_address, token_id);
        delete propCollection[token_id];
        collectionSize--;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI,
        string memory tokenJSON
        
    ) public returns (uint256) {
        propCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI, tokenJSON);

        return (propCollection[tokenId].appraisalValue);
    }
}
